#!/usr/bin/python3.5
# coding: ascii

## requires /usr/bin/pip3 install python-poppler-qt5
## For mac: sudo port install poppler-qt5

import popplerqt5
import os, sys, urllib
import PyQt5


SUMM  = "Summary"             # Purple 
DNU   = "Did not understand"  # Red
NOTE  = "Note"                # Yellow
QUOTE = "Quote"               # Quote/Highlight
CITE  = "New Source"          # Cite

color_dict = {226 : SUMM,  # Purple 
              253 : DNU,   # Red/Pink
              248 : NOTE,  # Yellow
              255 : NOTE,  # Yellow
              178 : QUOTE, # Green
              188 : QUOTE, # Green
              164 : CITE,  # Blue
              165 : CITE   # Blue
             }


def main(filename, basepage = 1, quiet = False):

    doc = popplerqt5.Poppler.Document.load(filename)

    n_pages = doc.numPages()

    annotations = []

    for i in range(n_pages):

        #########
        ## Now use the popplerqt5 interface to get the highlights....
        ## following http://stackoverflow.com/questions/21050551/
        ## and https://people.freedesktop.org/~aacid/docs/qt5/classPoppler_1_1Annotation.html

        page = doc.page(i)
        (pwidth, pheight) = (page.pageSize().width(), page.pageSize().height())

        for annotation in page.annotations():

            # popplerqt5.Poppler.TextAnnotation
            # popplerqt5.Poppler.HighlightAnnotation
            if annotation.subType() not in [1, 4]: continue
               
            note = {}
            note["page"]    = basepage+i
            note["note"]    = annotation.contents()
            note["text"]    = ""

            try: note["context"] = color_dict[annotation.style().color().red()]
            except KeyError:

                print("Do not have color (r, g, b) = ({}, {}, {})".format( 
                      annotation.style().color().red(),
                      annotation.style().color().green(),
                      annotation.style().color().blue()))

                sys.exit()

            # retrieving the highlight is a bit more finnicky,
            # since PDFs aren't really designed for this.
            if isinstance(annotation, popplerqt5.Poppler.HighlightAnnotation):

                for quad in annotation.highlightQuads():
                    rect = (quad.points[0].x() * pwidth, quad.points[0].y() * pheight,
                            quad.points[2].x() * pwidth, quad.points[2].y() * pheight)

                    bdy = PyQt5.QtCore.QRectF()
                    bdy.setCoords(*rect)
                    note["text"] += page.text(bdy) + " "

            annotations.append(note)

    with open(filename.replace(".pdf", ".txt"), "w") as out:

        out.write("#### Notes for " + filename + "\n\n")

        if any([v["context"] == SUMM for v in annotations]):
            out.write("Summary Impressions :: \n")
            for v in annotations:
                if v["context"] is SUMM:
                    out.write("{note}\n".format(**v))
            out.write("\n\n")

        if any([v["context"] == CITE for v in annotations]):
            out.write("Additional sources to check out :: \n")
            for v in annotations:
                if v["context"] is CITE:
                    if v["note"]: out.write("{note}\n".format(**v))
                    out.write(" >> {text}\n\n".format(**v))
            out.write("\n\n")
                
        if any([v["context"] == DNU for v in annotations]):
            out.write("Did not understand :: \n")
            for v in annotations:
                if v["context"] is DNU:
                    out.write("{note}\n".format(**v))
                    out.write(" >> {text}\n\n".format(**v))
            out.write("\n\n")
                
        for v in annotations:
            out.write("Notes and Quotes :: \n")
            if v["context"] in [NOTE, QUOTE]:
                s = "{page:>4d}".format(**v)
                if v["context"] == NOTE:  s+= " :N: "
                if v["context"] == QUOTE: s+= " :Q: "
                if v["note"]: s += "{note}".format(**v)
                if v["text"]: s += " >>>> \"\"{text}\"\"".format(**v)
                s += "\n"

                out.write(s)

    if not quiet:
        with open(filename.replace(".pdf", ".txt"), "r") as out:
            for l in out: print(l[:-1])


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("-p", "--pages", type=int, default = 1)
    parser.add_argument("-q", "--quiet", action="store_true")
    args = parser.parse_args()

    main(args.filename, args.pages, args.quiet)


