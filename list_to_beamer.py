#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Make the beamer file for a set of plots
"""

import sys
import os
import string

from ltb_helper import accDict, grDict, symDict, SymbolReplacement, ModifierReplacement

prologue = """
\documentclass[dvipsnames,table]{beamer}
  
\usetheme{jamiesimple}
\usepackage{type1cm}
\usepackage{bm}
\usepackage{ulem}
\usepackage{subfigure}
\usepackage{multicol}
\usepackage{slashed}
\usepackage{braket}
\usepackage{epstopdf}
\usepackage{grffile}
\usepackage{soul}
\usepackage{multirow}
\usepackage{rotating}
\usepackage{color}
\usepackage{xcolor,colortbl}
\usepackage{hyperref}
\usepackage{wasysym}
\usepackage{appendixnumberbeamer}
\usepackage{rotating}
\usepackage[outline]{contour} 
\usepackage{gensymb}
\usepackage{arydshln}

\usepackage[listings,theorems]{tcolorbox}
\\tcbset{colback=chlgr,colframe=chdgr}

\usepackage{pifont}

\usepackage[absolute, overlay]{textpos}
\TPGrid{100}{100}

\contourlength{0.15em}
\contournumber{27}

\let\oldfootnotesize\\footnotesize
\\renewcommand*{\\footnotesize}{\oldfootnotesize\\tiny}


%% args are: slide iteration, size, x, y, angle, text
\definecolor{caveatcolor}{rgb}{0.584, 0, 0.102}
\\newcommand{\\caveat}[6]{\only<#1> {\\begin{textblock}{40}[0.,0.](#3,#4)\\begin{rotate}{#5} \\textbf{\\textcolor{caveatcolor}{\contour{white}{\\fontsize{#2}{#2}\selectfont #6}}} \end{rotate}\end{textblock}}}

\\newcommand{\placegraphic}[4]{\\begin{textblock}{20}[0.5,0.5](#1,#2)\includegraphics[width=#3]{#4}\end{textblock}}

\\newenvironment{changemargin}[2]{
    \\begin{list}{}{%%
        \setlength{\\topsep}{0pt}%%
        \setlength{\leftmargin}{#1}%%
        \setlength{\\rightmargin}{#2}%%
        \setlength{\listparindent}{\parindent}%%
        \setlength{\itemindent}{\parindent}%%
        \setlength{\parsep}{\parskip}%%
    }%%
    \item[]
}{
    \end{list}
}

\\newcommand{\\fixme}{\\textbf{\\textcolor{red}{[FIXME!]}}}
\\renewcommand{\\note}[1]{\\textbf{\\textcolor{red}{[#1]}}}

\usepackage{xspace}
\usepackage{upgreek}
\\newcommand{\cm}{\ensuremath{~\\text{cm}}\\xspace}
\\newcommand{\um}{\ensuremath{~\upmu\\text{m}}\\xspace}
\\newcommand{\us}{\ensuremath{~\upmu\\text{s}}\\xspace}

\\newcommand{\colbox}[1]{\\begin{tcolorbox}#1\end{tcolorbox}}

\\newcommand{\\chred}[1]{\\textbf{\\textcolor{chred}{#1}}}
\\newcommand{\\chdgr}[1]{\\textbf{\\textcolor{chdgr}{#1}}}
\\newcommand{\\chlgr}[1]{\\textbf{\\textcolor{chlgr}{#1}}}
\\newcommand{\\pennred}[1]{\\textbf{\\textcolor{pennred}{#1}}}
\\newcommand{\\pennblue}[1]{\\textbf{\\textcolor{pennblue}{#1}}}
\\newcommand{\\cernblue}[1]{\\textbf{\\textcolor{cernblue}{#1}}}
\\newcommand{\\infnblue}[1]{\\textbf{\\textcolor{infnblue}{#1}}}
\\newcommand{\\red}[1]{\\textbf{\\textcolor{red}{#1}}}
\\newcommand{\\orange}[1]{\\textbf{\\textcolor{orange}{#1}}}
\\newcommand{\\gold}[1]{\\textbf{\\textcolor{gold}{#1}}}

\colorlet{darkgreen}{black!30!blue!25!green}
\\renewcommand{\\red}[1]{\\textbf{\\textcolor{red}{#1}}}
\\newcommand{\\yellow}[1]{\\textbf{\\textcolor{yellow}{\contour{black}{#1}}}}
\\newcommand{\\green}[1]{\\textbf{\\textcolor{darkgreen}{#1}}}
\\newcommand{\\blue}[1]{\\textbf{\\textcolor{blue}{#1}}}
\\newcommand{\\black}[1]{\\textbf{\\textcolor{black}{#1}}}
\\newcommand{\\purple}[1]{\\textbf{\\textcolor{purple}{#1}}}
\\newcommand{\\magenta}[1]{\\textbf{\\textcolor{magenta}{#1}}}
\\newcommand{\\grey}[1]{\\textbf{\\textcolor{gray}{#1}}}
\\newcommand{\\white}[1]{\\textbf{\\textcolor{white}{#1}}}

\\newcommand{\\twoVec}[2]{\ensuremath{\\begin{pmatrix}#1\\\\#2\end{pmatrix}}}
\\newcommand{\\twoMat}[4]{\ensuremath{\\begin{pmatrix}#1 & #2\\\\#3 & #4\end{pmatrix}}}
\\newcommand{\\twoSm}[2]{\ensuremath{\left (\\begin{smallmatrix}#1\\\\#2\end{smallmatrix} \\right)}}

\\newcommand{\pcell}[2][c]{\\begin{tabular}[#1]{@{}c@{}}#2\end{tabular}}

\\newcolumntype{P}[1]{>{\centering\\arraybackslash}p{#1}}
\\newcolumntype{M}[1]{>{\centering\\arraybackslash}m{#1}}
\\newcommand{\cg}{\cellcolor{green}}
\\newcommand{\cy}{\cellcolor{yellow}}
\\newcommand{\\ry}{\\rowcolor{yellow}}
\\newcommand{\co}{\cellcolor{orange}}
\\newcommand{\cb}{\cellcolor{infnblue}}

\\renewcommand{\\tt}[1]{\\texttt{#1}}
\\renewcommand{\_}{\\texttt{\detokenize{_}}}
\\newcommand{\unsim}{\\raisebox{.25ex}{\ensuremath{\mbox{\scriptsize $\sim\,$}}}}
\\renewcommand{\\L}{\\mathcal{L}}
\\renewcommand{\O}{\\mathcal{O}}
\\newcommand{\\tss}[1]{\\textsuperscript{#1}}

\usepackage{upquote,textcomp}
\\newcommand{\\tqs}{\\textquotesingle{}}

\\newcommand{\pr}{\ensuremath{\\blacksquare}~}

\\newcommand{\half}{\\frac{1}{2}}
\\newcommand{\\thus}{\\Longrightarrow}
\\newcommand{\\Thus}{\hspace{0.25em}\\Longrightarrow\hspace{0.25em}}
\\renewcommand{\\and}{\\text{\hspace{0.25in}and\hspace{0.25in}}}
\\newcommand{\singleImage}[1]{
  \\begin{changemargin}{-1cm}{-1cm}
  \\begin{center}
  \includegraphics[width=\paperwidth,height=0.98\paperheight,keepaspectratio]{#1}
  \end{center}
  \end{changemargin}
}
\\newcommand{\\pder}[2]{\\frac{\partial #1}{\partial #2}}
\\newcommand{\met}{E_\\text{T}^\\text{miss}}

\setul{0.1em}{0.07em}
\\newcommand{\link}[2]{\href{#1}{\chred{\ul{#2}}}}
\\newcommand{\\tright}[1]{\hskip0pt plus 1filll \small{#1}}

\\newcommand{\cmark}{\green{\ding{51}}}
\\newcommand{\\xmark}{\\red{\ding{55}}}

\usepackage{tikz}
\\newcommand{\pie}[2]{\\begin{tikzpicture}\draw[#2, thick] (0,0) circle(0.8ex); \\fill[#2, rotate=90] (0.8ex,0) arc (0:-#1:0.8ex) -- (0,0) -- cycle;\end{tikzpicture}}

\\newcolumntype{L}[1]{>{\\raggedright\let\\newline\\\\\\arraybackslash\hspace{0pt}}m{#1}}
\\newcolumntype{C}[1]{>{\centering\let\\newline\\\\\\arraybackslash\hspace{0pt}}m{#1}}
\\newcolumntype{R}[1]{>{\\raggedleft\let\\newline\\\\\\arraybackslash\hspace{0pt}}m{#1}}


\\renewcommand*{\\thefootnote}{\\fnsymbol{footnote}}



%s

\setbeamertemplate{navigation symbols}{}

%% ncols, size
\\bibliographystyle{beamer}

\\newcommand{\makebib}[2]{\\fontsize{#2}{#2} \selectfont
\setbeamertemplate{bibliography item}{[\\theenumiv]}
\\begin{multicols}{#1}
\\bibliography{sources}
\end{multicols}
}

\setbeamertemplate{itemize items}[default]
\setbeamertemplate{enumerate items}[default]
%%\let\emph\\textit

\\title[%s]{%s}
%s
\\author[%s]{%s}
\institute[%s]{%s}%s
\date{%s}


\\begin{document}


"""

linefrac = (1.,0.49,0.32,0.44,0.32,0.32,0.32,0.32,0.32)
perCol   = (1,1,1,2,2,2,3,3,3)

epilogue = "\end{document}"

begin_frame = "\\begin{frame}\n"
begin_plain_frame = "\\begin{frame}[plain]\n"
end_frame = "\end{frame}\n\n"

picext = ["pdf", "eps", "png", "jpg"]

side_frame = "\\vspace{-1.5em}\n\\begin{columns}\n\\begin{column}{%4.2f\\textwidth}%s\n\end{column}\n\n\\begin{column}{%4.2f\\textwidth}\n%s\end{column}\n\end{columns}\n\n"

def main(inputFileName, outputFileName):

  fileIN = open(inputFileName, "r")
  fileOUT = open(outputFileName, "w")

  title = ""
  short_title = ""
  author = "Jamie Saxon"
  short_author = "Saxon"
  institute = "University of Chicago"
  short_institute = "Chicago"
  logo = ""
  subtitle = ""
  TITLE = True
  date = "\\today"
  header = ""

  line = fileIN.readline()
  while line[0] is "^":

    # line = ModifierReplacement(line)
    line = line.decode('utf-8')
    line = ModifierReplacement(line)
    line = SymbolReplacement(line)

    if line[:3] == "^T:":
      title = line[3:].strip()
    if line[:3] == "^A:":
      author = line[3:].strip()
    if line[:3] == "^I:":
      institute = line[3:].strip()
    if line[:3] == "^D:":
      date = line[3:].strip()
    if line[:4] == "^ST:":
      short_title = line[4:].strip()
    if line[:3] == "^M:":
      subtitle = "\n\subtitle{%s}\n" % line[3:].strip()
    if line[:4] == "^SA:":
      short_author = line[4:].strip()
    if line[:4] == "^SI:":
      short_institute = line[4:].strip()
    if line[:3] == "^L:":
      logo_graph = ""
      spline = line[3:].split(",")
      for i in spline:
        s = 3
        if len(i.split(":")) > 2:
          s = float(i.split(":")[1])
        p = i.split(":")[0].strip()
        if logo_graph != "":
          logo_graph += "\hspace{2em}"
        logo_graph += "\includegraphics[height=%.1fem]{%s}" % (s, p)
      logo = "\n\\titlegraphic{%s}\n" % logo_graph
    elif line[:2] == "^L":
      logo = "\n\\titlegraphic{\includegraphics[height=2.5em]{../zBeamer/chicago.pdf}}\n"
    if line[:3] == "^NT":
      TITLE = False
    if line[:3] == "^H:":
      header += line[3:].strip() + "\n"
    line = fileIN.readline()

  if short_title == "":
    short_title = title

  fileOUT.write(prologue % (header, short_title, title, subtitle, short_author, author, short_institute, institute, logo, date))
  if TITLE:
    fileOUT.write("\n\\begin{frame}\n\\titlepage\n\end{frame}\n\n\n")

  frame_title = ""
  frame_opt = ""
  title = ""
  label = ""
  graphic_string = ["", ""]
  graphic_string_side = ""
  table = ""
  table_title = ""
  table_size = ""
  chat = ""
  side = False
  side_table = False
  single = False
  backup = False
  
  line = fileIN.readline()
  while line: 

    line = line.decode('utf-8')
    line = ModifierReplacement(line)
    line = SymbolReplacement(line)

    if line == "\\backup":
      backup = True
    elif (string.find(line, "+++") == 0): # section head?
      secName = line[3:].strip()
      secName = secName.replace("\\","")
      secName = secName.replace("$slashed{E} _{T } $","MET")
      secName = secName.replace("$slashed{E}_{T } $","MET")
      secName = secName.replace("text","")
      secName = secName.replace("bm","")
      secName = secName.replace("_","")
      secName = secName.replace("{","")
      secName = secName.replace("}","")

      embold = ""
      for ei, e in enumerate(line[3:].strip().split("$")):
        if (ei % 2) == 1:
          e = "$\\bm{" + e + "}$"
        embold += e

      chat += "\\begin{tcolorbox}[colback=chlgr,colframe=chdgr]\n\\begin{center}\n\huge{\\textbf{%s}}\n\section{%s}\n\end{center}\n\end{tcolorbox}\n\n" % (embold, secName)

    elif (string.find(line, "++") == 0): # subsection head?
      secName = line[2:].strip()
      secName = secName.replace("\\","")
      secName = secName.replace("$slashed{E} _{T } $","MET")
      secName = secName.replace("$slashed{E}_{T } $","MET")
      secName = secName.replace("text","")
      secName = secName.replace("bm","")
      secName = secName.replace("_","")
      secName = secName.replace("{","")
      secName = secName.replace("}","")

      embold = ""
      for ei, e in enumerate(line[2:].strip().split("$")):
        if (ei % 2) == 1:
          e = "$\\bm{" + e + "}$"
        embold += e

      chat += "\\begin{tcolorbox}[colback=chlgr,colframe=chdgr]\n\\begin{center}\n\Large{\\textbf{%s}}\n\subsection{%s}\n\end{center}\n\end{tcolorbox}\n\n" % (embold, secName)

    elif (string.find(line, "+L:") == 0): # store a label if there is one
      label = line[3:].strip()
    elif (string.find(line, "+") == 0): # store a title if there is one
      frame_opt = ""
      if string.find(line, "[") == 1:
        frame_opt = line[string.find(line, "["):string.find(line, "]")+1]
        title = line[string.find(line, "]")+1:].strip()
      else: title = line[1:].strip()
    elif (string.find(line, "@") == 0): # link
      chat += "\\begin{center}"
      if line[1] == ":":
        val = float(line.split()[0].split(":")[1])
        chat += "\\fontsize{%.1f}{%.1f}\selectfont" % (val, val+1.5)
      chat += "\\url{%s}\\normalsize \end{center}\n" % line.split()[1]
    elif (".eps" in line or \
          ".pdf" in line or \
          ".png" in line or \
          ".jpg" in line) and \
         ":side" not in line:
      files = line.split(";")

      pos = 1 if (not ":up" in line) else 0

      graphic_string[pos] += "\\begin{columns}[c]\n"
  
      currFile = 0
      for x in files:
        if currFile % perCol[len(files) - 1] == 0:
          width = 1.
          ysp = [y for y in x.split() if any([(m in y) for m in picext])]
          if len(ysp):
            ysp = ysp[0].split(":")
            width = 1. if len(ysp) == 1 else float(ysp[1])
          graphic_string[pos] += "\\begin{column}{%.2f\linewidth}\n\\begin{center} \\fontsize{8.5}{9.2} \selectfont " % (width * linefrac[len(files) - 1])
        for y in x.split(): # allow for off-the-cuff comments.
          if y.find("eps") == -1 and \
             y.find("pdf") == -1 and \
             y.find("png") == -1 and \
             y.find("jpg") == -1:
            graphic_string[pos] += y.strip() + " "
          else:
            ysp = y.split(":")
            # width = 1. if len(ysp) == 1 else float(ysp[1])
            graphic_string[pos] += "\n\includegraphics[width=%4.2f\linewidth]{%s} \\\\  " % (1.0, ysp[0]) # (width, ysp[0])
            if "full" in ysp:
              single = "\singleImage{%s}" % ysp[0]
          if title == "": #if there is no explicit title use the filename
            title = string.replace(y[:len(y)-4], "_", " ")
        currFile += 1
        if currFile % perCol[len(files) - 1] == 0 or currFile == len(files):
          graphic_string[pos] += "\n\end{center}\n\end{column}\n"
      graphic_string[pos] += "\end{columns}\n\n"
    elif (".eps" in line or \
          ".pdf" in line or \
          ".png" in line or \
          ".jpg" in line) and \
         ":side" in line:

      files = line.split(";")

      graphic_string_side = "\n\\begin{center} \\fontsize{10}{10.5} \selectfont "
  
      currFile = 0
      for x in files:

        for y in x.split(): # allow for off-the-cuff comments.

          if ".eps" not in y and \
             ".pdf" not in y and \
             ".png" not in y and \
             ".jpg" not in y:
            graphic_string_side += y.strip() + " "
          else:
            ysp = y.split(":")
            side = float(ysp[1])
            graphic_string_side += "\n\includegraphics[width=\linewidth]{%s} \\\\ " % ysp[0]
      graphic_string_side += "\n\end{center} \n"
    elif (string.find(line, "`") == 0):
      chat += "\colbox{\\texttt{%s}}\n" % line[1:].strip()
    elif (string.find(line, "'''") == 0):
      chat += "\colbox{%s}\n" % line[3:].strip()
    elif (string.find(line, "---") == 0):
      chat += "\\begin{itemize}\n\\begin{itemize}\n\\begin{itemize}\n  \item %s \n\end{itemize}\n\end{itemize}\n\end{itemize}\n" % line[3:].strip()
    elif (string.find(line, "--") == 0):
      chat += "\\begin{itemize}\n\\begin{itemize}\n\item %s \n\end{itemize}\n\end{itemize}\n" % line[2:].strip()
    elif (string.find(line, "#--") == 0):
      chat += "\\begin{enumerate}\n\\begin{itemize}\n\\begin{itemize}\n  \item{%s}\n\end{itemize}\n\end{itemize}\n\end{enumerate}\n" % line[3:].strip()
    elif (string.find(line, "#-") == 0):
      chat += "\\begin{enumerate}\n\\begin{itemize}\n\item{%s}\n\end{itemize}\n\end{enumerate}\n" % line[2:].strip()
    elif (string.find(line, "-#-") == 0):
      chat += "\\begin{itemize}\n\\begin{enumerate}\n\\begin{itemize}\n   \item{%s}\n\end{itemize}\n\end{enumerate}\n\end{itemize}\n" % line[3:].strip()
    elif (string.find(line, "-#") == 0):
      chat += "\\begin{itemize}\n\\begin{enumerate}\n   \item{%s}\n\end{enumerate}\n\end{itemize}\n" % line[2:].strip()
    elif (string.find(line, "-") == 0):
      chat += "\\begin{itemize}\n\item %s\n\end{itemize}\n" % line[1:].strip()
    elif (string.find(line, "#") == 0): 
      chat += "\\begin{enumerate}\n\item %s\n\end{enumerate}\n" % line[1:].strip()
    elif (string.find(line, "*") == 0):
      if string.find(line, "*T:") == 0:
        table_title = line[3:].strip()
      elif string.find(line, "*S:") == 0:
        side = float(line[3:].strip())
        side_table = True
      elif string.find(line, "*F:") == 0:
        size = float(line[3:].strip())
        table_size = "\\fontsize{%.1f}{%.1f} \\selectfont\n" % (size, size+3)
      elif not table:
        table = "\\begin{center}\n\\begin{tabular}{%s}\n\hline\n\hline\n" % line[1:].strip()
      else:
        table += line[1:] + "\n"
    elif (string.find(line, ">") == 0):
      chat += "\\vspace{%s}\n" % line[1:].strip()
    elif (string.find(line, "<") == 0):
      chat += "\\vspace{-%s}\n" % line[1:].strip()
    elif line == "": # the slide is finished, so write it.

      begin_frame = "\\begin{frame}"
      if label: begin_frame +="[label=%s]" % label
      if frame_opt: begin_frame += frame_opt
      begin_frame += "\n"

      if title:
        frame_title = "\\frametitle{" + title + "}"
        frame_title += "\n\n"

      if table:
        if table_size:
          table = table_size + table
        if table_title != "":
          table_title = "\\\\\n\\vspace{0.2em}" + table_title + "\n"
        table += "\hline\n\hline\n\end{tabular}\n%s\n\end{center}\\vspace{-2em}" % table_title

      chat = string.replace(chat, "\end{itemize}\n\\begin{itemize}\n", "")
      chat = string.replace(chat, "\end{enumerate}\n\\begin{enumerate}\n", "")
      chat = string.replace(chat, "\end{itemize}\n\\begin{itemize}\n", "")
      chat = string.replace(chat, "\end{itemize}\n\\begin{itemize}\n", "")

      try: 
        if "\end{document}" in chat:
          break
        if side:
          if side_table:
            left = graphic_string[0] + chat + graphic_string[1]
            right = graphic_string_side + table
          else:
            left = graphic_string[0] + chat + graphic_string[1] + table
            right = graphic_string_side
          fileOUT.write(begin_frame + frame_title + (side_frame % (1-side, left, side, right)) + end_frame)
        elif single:
          fileOUT.write(begin_plain_frame + single + chat + end_frame)
        elif backup:
          fileOUT.write("\\appendix\n" + begin_frame + frame_title + graphic_string[0] + chat + table + graphic_string[1] + end_frame)
        else:
          fileOUT.write(begin_frame + frame_title + graphic_string[0] + chat + table + graphic_string[1] + end_frame)
      except:

        print "PROBLEM AT SLIDE:", frame_title.strip()
        print line
        raise

      begin_frame = ""
      frame_title = ""
      title = ""
      frame_opt = ""
      label = ""
      graphic_string = ["", ""]
      graphic_string_side = ""
      table = ""
      table_title = ""
      chat = ""
      side = False
      single = False
      backup = False

    elif (string.find(line, "!!") == 0):
      embold = ""
      for ei, e in enumerate(line[2:].strip().split("$")):
        if (ei % 2) == 1:
          e = "$\\bm{" + e + "}$"
        embold += e
      chat += "\\begin{tcolorbox}[colback=red,colframe=red]\n\\begin{center}\n\Large{\\white{%s}}\n\end{center}\n\end{tcolorbox}\n\n" % embold

    elif (string.find(line, "!") == 0):
      embold = ""
      for ei, e in enumerate(line[1:].strip().split("$")):
        if (ei % 2) == 1:
          e = "$\\bm{" + e + "}$"
        embold += e
      chat += "\\begin{tcolorbox} \n\\begin{center}\n\Large{\\textbf{%s}}\n\end{center}\n\end{tcolorbox}\n\n" % embold
    elif (string.find(line, "=") == 0):
      embold = ""
      for ei, e in enumerate(line[1:].strip().split("$")):
        if (ei % 2) == 1:
          e = "$\\bm{" + e + "}$"
        embold += e
      chat += "\\textbf{%s}" % embold
    else: # just include it on the slide.
      chat += line + "\n"

      
    line = fileIN.readline()
  
  fileOUT.write(epilogue)
  
  fileIN.close()
  fileOUT.close()

  os.system('pdflatex ' + outputFileName)


#----------------------------------------------------
if __name__ == "__main__":
    from optparse import OptionParser

    p = OptionParser()
    p.add_option('-i', '--in', type = 'string', dest = 'inputFile', help = 'input File' )
    p.add_option('-o', '--out', type = 'string', dest = 'outputFile', default = "", help = 'output File' )

    (options,args) = p.parse_args()

    if options.outputFile == "":
      options.outputFile = options.inputFile + ".tex"

    main(options.inputFile, options.outputFile)

