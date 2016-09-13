#!/usr/bin/env python3
# coding: ascii

import popplerqt5
import os, sys, urllib
import PyQt5


DNU  = "Did not understand"
NOTE = "Note"
HLT  = "Highlight"
CITE = "New Source"
color_dict = {253 : DNU, 248 : NOTE, 178 : HLT, 164 : CITE, 226 : None,
              188 : HLT, 165 : CITE}


def main(filename, basepage = 0):

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
            if annotation.subType() not in [1, 4]:
                continue
               
            note = {}
            note["page"]    = i+1
            note["note"]    = annotation.contents()
            note["text"]    = ""

            try:

                note["context"] = color_dict[annotation.style().color().red()]

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

        out.write("#### Notes for " + filename + "\n\n\n")

        if any([v["context"] == DNU for v in annotations]):
            out.write("Did not understand :: \n")
            for v in annotations:
                if v["context"] in [DNU]:
                    out.write("{note}\n".format(**v))
                    out.write(" >> {text}\n\n".format(**v))
            out.write("\n\n")
                
        if any([v["context"] == CITE for v in annotations]):
            out.write("Additional sources to check out :: \n")
            for v in annotations:
                if v["context"] in [CITE]:
                    if v["note"]: out.write("{note}\n".format(**v))
                    out.write(" >> {text}\n\n".format(**v))
            out.write("\n\n")
                
        for v in annotations:
            if v["context"] in [DNU, NOTE, HLT]:
                s = "{page:4} ".format(**v)
                if v["note"]: s += " :: {note}".format(**v)
                if v["text"]: s += " >>>> \"\"{text}\"\"".format(**v)
                s += "\n"

                out.write(s)


if __name__ == "__main__":

    main(sys.argv[1])


