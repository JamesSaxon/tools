#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import string

graphs = ["eps", "pdf", "png", "jpg"]

FORMAT = None
TYPES = { 
           "equation"         : [  1, "$",    "\[ %s \]"], 
           "numequation"      : [  2, "#$",   "\\begin{equation}  %s \n\end{equation}"],
           "boxed"            : [  3, "!",    "\[ \\boxed{ %s } \]"],
           "subsubsectionstar": [  4, ">>>*", "\subsubsection*{%s}"],
           "subsectionstar"   : [  5, ">>*",  "\subsection*{%s}"],
           "sectionstar"      : [  6, ">*",   "\section*{%s}"],
           "subsubsubsection" : [  7, ">>>>", "\\vspace{0.5em}\\noindent\emph{%s}"],
           "subsubsection"    : [  8, ">>>",  "\subsubsection{%s}"],
           "subsection"       : [  9, ">>",   "\subsection{%s}"],
           "section"          : [ 10, ">",    "\section{%s}"],
           "subsubsubitem"    : [ 11, "----", "\\begin{itemize}\n\\begin{itemize}\n\\begin{itemize}\n\\begin{itemize}\n    \item  %s \n\end{itemize}\n\end{itemize}\n\end{itemize}\n\end{itemize}"],
           "subsubitem"       : [ 12, "---",  "\\begin{itemize}\n\\begin{itemize}\n\\begin{itemize}\n   \item  %s \n\end{itemize}\n\end{itemize}\n\end{itemize}"],
           "subitemenum"      : [ 13, "--#",  "\\begin{itemize}\n\\begin{itemize}\n\\begin{enumerate}\n   \item  %s \n\end{enumerate}\n\end{itemize}\n\end{itemize}"],
           "subitem"          : [ 14, "--",   "\\begin{itemize}\n\\begin{itemize}\n  \item  %s \n\end{itemize}\n\end{itemize}"],
           "itemenum"         : [ 15, "-#",   "\\begin{itemize}\n\\begin{enumerate} \item  %s \end{enumerate}\n\end{itemize}"],
           "item"             : [ 16, "-",    "\\begin{itemize}\n\item  %s \n\end{itemize}"],
           "numalign"         : [ 17, "#@",   "\\begin{align}\n %s \end{align}"],
           "enumii"           : [ 18, "#--",  "\\begin{enumerate}\n\\begin{itemize}\n\\begin{itemize}\n \item  %s \n\end{itemize}\n\end{itemize}\n\end{enumerate}"],
           "enumi"            : [ 19, "#-",   "\\begin{enumerate}\n\\begin{itemize}\n \item  %s \n\end{itemize}\n\end{enumerate}"],
           "enum"             : [ 20, "#",   "\\begin{enumerate}\n\item  %s \n\end{enumerate}"],
           "align"            : [ 21, "@",   "\\begin{align*}\n %s \end{align*}"]
        }


appendix = False

prologue= """
\documentclass[%d pt]{%s}
\usepackage[top=%.2fin,bottom=%.2fin,left=%.2fin,right=%.2fin]{geometry}
%%\documentclass[11pt,reqno]{amsart}
%%\usepackage[top=1.8cm,bottom=1.8cm,left=1.8cm,right=1.8cm]{geometry}
\usepackage{amssymb, amsmath, bm}
\usepackage{mathabx}
\usepackage{indentfirst}
\usepackage{grffile}
\usepackage{multicol}
\usepackage{multirow}
\usepackage{xcolor,colortbl}
\usepackage{braket}
\usepackage{pifont}
\usepackage{cancel}
\usepackage{slashed}
\usepackage[final]{pdfpages}
\usepackage{multicol}
\usepackage[caption = false]{subfig}
\usepackage{simplewick}
\usepackage{cite}
\usepackage{hyperref}
\usepackage{wasysym}
\usepackage{setspace}

\\renewcommand{\_}{\\texttt{\detokenize{_}}}
\\renewcommand{\\and}{\\text{\hspace{0.25in}and\hspace{0.25in}}}
\\newcommand{\Thus}{\hspace{0.25in}\Longrightarrow\hspace{0.25in}}
\\newcommand{\\thus}{\Longrightarrow}
\\newcommand{\half}{\ensuremath{\\tfrac{1}{2}}}
\\newcommand{\pder}[2]{\ensuremath{\\frac{\partial #1}{\partial #2}}}
\\newcommand{\der}[2]{\ensuremath{\\frac{d #1}{d #2}}}
\\newcommand{\psder}[2]{\ensuremath{\\frac{\partial^2 #1}{\partial #2 {}^2}}}
\\newcommand{\mat}[1]{\ensuremath{\\begin{pmatrix}#1\end{pmatrix}}}
\\newcommand{\smMat}[1]{\ensuremath{\left(\\begin{smallmatrix}#1\end{smallmatrix}}\\right)}
\\newcommand{\\twoVec}[2]{\ensuremath{\\begin{pmatrix}#1\\\\#2\end{pmatrix}}}
\\newcommand{\\twoMat}[4]{\ensuremath{\\begin{pmatrix}#1 & #2\\\\#3 & #4\end{pmatrix}}}
\\newcommand{\\twoSm}[2]{\ensuremath{\left (\\begin{smallmatrix}#1\\\\#2\end{smallmatrix} \\right)}}
\\newcommand{\Ham}{\ensuremath{\mathcal{H}}}
\\newcommand{\Lg}{\ensuremath{\mathcal{L}}}
\\newcommand{\M}{\ensuremath{\mathcal{M}}}
\\renewcommand{\P}{\ensuremath{\mathcal{P}}}
\\newcommand{\T}{\ensuremath{\mathcal{T}}}
\\newcommand{\F}{\ensuremath{\mathcal{F}}}
\\newcommand{\J}{\ensuremath{\mathcal{J}}}
\\newcommand{\E}{\ensuremath{\mathcal{E}}}
\\renewcommand{\O}{\ensuremath{\mathcal{O}}}
\\newcommand{\\tss}[1]{\\textsuperscript{#1}}
\\newcommand{\\real}{\\text{Re}}
\\newcommand{\imag}{\\text{Im}}
\\newcommand{\sgn}{\\text{sgn}}
\\newcommand{\Tr}{\\text{Tr}}
\\renewcommand{\d}{\hspace{0.25em}\\text{d}\hspace{-0.05em}}
\\newcommand{\\xmark}{\ding{55}}
\\newcommand{\inb}{\ensuremath{\\text{~nb\\tss{-1}}}}
\\newcommand{\ifb}{\ensuremath{\\text{~fb\\tss{-1}}}}
\\newcommand{\iab}{\ensuremath{\\text{~ab\\tss{-1}}}}
\\newcommand{\ipb}{\ensuremath{\\text{~pb\\tss{-1}}}}
\\newcommand{\gev}{\\text{~GeV}}
\\newcommand{\mev}{\\text{~MeV}}
\\newcommand{\\tev}{\\text{~TeV}}

\usepackage{xspace}
\usepackage{upgreek}
\\newcommand{\cm}{\ensuremath{~\\text{cm}}\\xspace}
\\newcommand{\um}{\ensuremath{~\upmu\\text{m}}\\xspace}
\\newcommand{\us}{\ensuremath{~\upmu\\text{s}}\\xspace}
\\newcommand{\mm}{\ensuremath{~\\text{mm}}\\xspace}


\\newcommand{\\missing}{\\textbf{\\textcolor{red}{[MISSING!]}}}
\\newcommand{\\fixme}{\\textbf{\\textcolor{red}{[FIXME!]}}}
\\newcommand{\\note}[1]{\\textbf{\\textcolor{red}{[#1]}}}

\\newcommand{\wick}[4]{\contraction[0.25em]{#1}{#2}{#3}{#4}}
\\newcommand{\unsim}{\ensuremath{\mbox{$\sim$}}}

\\newcommand{\met}{E_\\text{T}^\\text{miss}}
\\newcommand{\metTr}{E_\\text{T}^\\text{miss, Truth}}
\\newcommand{\metRe}{E_\\text{T}^\\text{miss, Reco.}}

\\newcommand{\pT}{p_\\text{T}}
\\newcommand{\pt}{p_\\text{T}}

\\newlength\dlf\\newcommand\\alignedbox[2]{
  &
  \\begingroup
  \settowidth\dlf{$\displaystyle #1$}
  \\addtolength\dlf{\\fboxsep+\\fboxrule}
  \hspace{-\dlf}
  \\boxed{#1\hspace{0.008in}=\hspace{0.008in} #2}
\endgroup
}

\usepackage{tikz}
\usetikzlibrary{svg.path}
%% \\newcommand{\cbox}{\\begin{tikzpicture}\draw[thick] (0,0) square(1.0ex); \end{tikzpicture}}
\\newcommand{\pie}[2]{\\begin{tikzpicture} \draw[thick] (0,0) rectangle ++(1.5ex,1.5ex);\end{tikzpicture}}
 
\hypersetup{
    colorlinks=true,linkcolor=blue,citecolor=blue,urlcolor=blue,
        pdftitle={%s},
          pdfauthor={%s}
      pdfpagemode={UseOutlines},
          bookmarksopen=true,bookmarksnumbered=true,pdfstartview={Fit}
}

\\newcommand{\link}[2]{\href{#1}{\\textcolor{blue}{#2}}}

%% header
%s  


%%\\renewcommand*\\theenumi{\\Alph{enumi}}
\\renewcommand*\labelenumi{(\\theenumi)}
\\renewcommand{\labelitemi}{$\\blacktriangleright$}
\\renewcommand{\labelitemiii}{$-$}
\\renewcommand{\labelitemiv}{$-$}


\\title[%s]{%s}
\date{\\today}
\\author[%s]{%s}

\\begin{document}

%s

"""

epilogue = "\n\n\end{document}\n\n"


parDict = {
  ")": "\\right) ", 
  "(": "\left( ", 
  "]": "\\right] ", 
  "[": "\left[ ", 
  "{": "left\{ ", 
  "}": "right\} "
}

symDict = {
  "½".decode('utf-8'): "\half ", 
  "ℚ".decode('utf-8'): "\mathbb{Q} ", 
  "ℤ".decode('utf-8'): "\mathbb{Z} ", 
  "×".decode('utf-8'): "\\times ", 
  "≥".decode('utf-8'): "\geq ", 
  "≤".decode('utf-8'): "\leq ", 
  "→".decode('utf-8'): "\\rightarrow ", 
  "⇒".decode('utf-8'): "\Thus ", 
  "∫".decode('utf-8'): "\int ", 
  "∮".decode('utf-8'): "\oint ", 
  "·".decode('utf-8'): "\cdot ", 
  "±".decode('utf-8'): "\pm ", 
  "∓".decode('utf-8'): "\mp ", 
  "✔".decode('utf-8'): "\checkmark ", 
  "≈".decode('utf-8'): "\\approx ", 
  "≡".decode('utf-8'): "\equiv ", 
  "∝".decode('utf-8'): "\propto ", 
  "∈".decode('utf-8'): "\in ", 
  "≠".decode('utf-8'): "\neq ", 
  "∞".decode('utf-8'): "\infty ", 
  "√".decode('utf-8'): "\sqrt ", 
  "ħ".decode('utf-8'): "\hbar ", 
  "∇".decode('utf-8'): "\\nabla ", 
  "Ɇ".decode('utf-8'): "\slashed{E} ", 
  "ℋ".decode('utf-8'): "\mathcal{H} ", 
  "ℒ".decode('utf-8'): "\mathcal{L} ", 
  "𝒪".decode('utf-8'): "\mathcal{O} ", 
  "∂".decode('utf-8'): "\partial ", 
  "ℓ".decode('utf-8'): "\ell ",
  "÷".decode('utf-8'): "\\frac",
  "□".decode('utf-8'): "\pie{0}{red}",
}

grDict = {
  "α".decode('utf-8'): "\\alpha ",
  "β".decode('utf-8'): "\\beta ",
  "ψ".decode('utf-8'): "\psi ",
  "δ".decode('utf-8'): "\delta ",
  "ε".decode('utf-8'): "\\varepsilon ",
  "ϵ".decode('utf-8'): "\\varepsilon ",
  "φ".decode('utf-8'): "\\varphi ",
  "γ".decode('utf-8'): "\gamma ",
  "η".decode('utf-8'): "\eta ",
  "ι".decode('utf-8'): "\iota ",
  "ξ".decode('utf-8'): "\\xi ",
  "κ".decode('utf-8'): "\kappa ",
  "λ".decode('utf-8'): "\lambda ",
  "μ".decode('utf-8'): "\mu ",
  "µ".decode('utf-8'): "\mu ",
  "ν".decode('utf-8'): "\\nu ",
  "ο".decode('utf-8'): "\omicron ",
  "π".decode('utf-8'): "\pi ",
  "ρ".decode('utf-8'): "\\rho ",
  "σ".decode('utf-8'): "\sigma ",
  "τ".decode('utf-8'): "\\tau ",
  "θ".decode('utf-8'): "\\theta ",
  "ω".decode('utf-8'): "\omega ",
  "χ".decode('utf-8'): "\chi ",
  "υ".decode('utf-8'): "\upsilon ",
  "ζ".decode('utf-8'): "\zeta ",
  "Α".decode('utf-8'): "\Alpha ",
  "Β".decode('utf-8'): "\Beta ",
  "Ψ".decode('utf-8'): "\Psi ",
  "Δ".decode('utf-8'): "\Delta ",
  "Ε".decode('utf-8'): "\Epsilon ",
  "Φ".decode('utf-8'): "\Phi ",
  "Γ".decode('utf-8'): "\Gamma ",
  "Η".decode('utf-8'): "\Eta ",
  "Ι".decode('utf-8'): "\Iota ",
  "Ξ".decode('utf-8'): "\Xi ",
  "Κ".decode('utf-8'): "\Kappa ",
  "Λ".decode('utf-8'): "\Lambda ",
  "Μ".decode('utf-8'): "\Mu ",
  "Ν".decode('utf-8'): "\Nu ",
  "Ο".decode('utf-8'): "\Omicron ",
  "Π".decode('utf-8'): "\prod ",
  "Ρ".decode('utf-8'): "\Rho ",
  "Σ".decode('utf-8'): "\sum ",
  "Τ".decode('utf-8'): "\Tau ",
  "Θ".decode('utf-8'): "\Theta ",
  "Ω".decode('utf-8'): "\Omega ",
  "Χ".decode('utf-8'): "\Chi ",
  "Υ".decode('utf-8'): "\Upsilon ",
  "Ζ".decode('utf-8'): "\Zeta "
}

supDict = {
  "¹".decode('utf-8'): "^1 ",
  "²".decode('utf-8'): "^2 ",
  "³".decode('utf-8'): "^3 ",
  "⁴".decode('utf-8'): "^4 ",
  "⁵".decode('utf-8'): "^5 ",
  "⁶".decode('utf-8'): "^6 ",
  "⁷".decode('utf-8'): "^7 ",
  "⁸".decode('utf-8'): "^8 ",
  "⁹".decode('utf-8'): "^9 ",
  "⁰".decode('utf-8'): "^0 ",
  "✝".decode('utf-8'): "^\dagger ",
  #"*".decode('utf-8'): "^\star ",
  "⁺".decode('utf-8'): "^+ ",
  "⁻".decode('utf-8'): "^- "
}

subDict = {
  "₁".decode('utf-8'): "_1 ",
  "₂".decode('utf-8'): "_2 ",
  "₃".decode('utf-8'): "_3 ",
  "₄".decode('utf-8'): "_4 ",
  "₅".decode('utf-8'): "_5 ",
  "₆".decode('utf-8'): "_6 ",
  "₇".decode('utf-8'): "_7 ",
  "₈".decode('utf-8'): "_8 ",
  "₉".decode('utf-8'): "_9 ",
  "₀".decode('utf-8'): "_0 ",
  "ᵀ".decode('utf-8'): "_T ",
  "ᵢ".decode('utf-8'): "_i ",
  "ⱼ".decode('utf-8'): "_j ",
}

accDict = {
  "á".decode('utf-8'): "\\'a",
  "à".decode('utf-8'): "\`a",
  "é".decode('utf-8'): "\\'e",
  "è".decode('utf-8'): "\`e",
}

modDict = {
  u"\u20D7": "\\bm",
  u"\u0305": "\\overline",
  u"\u0307": "\dot",
  u"\u0308": "\ddot",
  u"\u0338": "\slashed",
  u"\u0303": "\\tilde",
  u"\u0302": "\\hat"
}

########################################
####  IS IT AN EQUATION, ETC.  #########
def GetSpecialFormat(line):

  decline = line.decode('utf-8')[0:-1]

  global FORMAT
  FORMAT = None

  t = TYPES.items()
  t.sort(key=lambda a: a[1][0])

  for key, val in t:

    if decline[0:len(val[1])] == val[1]:
      FORMAT = key
      decline = decline[len(val[1]):]
      break

  return decline

#########################################################
#########################################################

def ProcessFigure(line):

  figure = ""
  figCaption = []
  graphics, widths, subCaption, subLabel = [], [], [], []

  opt = ""
  if line[0] == "[":
    opt = line.split()[0][1:-1]
    line = line[line.find("]")+1:]

  # potential subfigures are split by ";"
  pieces = line.split(";")
  for p in pieces:

    # if there's a figure in this piece...
    if max([p.find("." + gri) for gri in graphs]) != -1:
      # worry about making subfigures.
      subCaption.append(" ")
      subLabel.append(" ")
      for word in p.split():
        pos = [word.find("." + graphs[i]) for i in range(len(graphs))]
        if max(pos) != -1:
          if word.find(":") != -1: 
            graphics.append(word[0:word.find(":")])
            widths.append(float(word[word.find(":")+1:]))
          else:
            graphics.append(word)
            widths.append(1.01)
        elif "label" in word:
          subLabel[-1] = word
        else:
          subCaption[-1] += word + " "
    elif p.strip is not "": # just add it to the figure caption.
      figCaption.append(p)
  figure = "\\begin{figure}[%s]" % opt
  if appendix:
    figure += "[h]"
  figure += "\n\centering\n"      
  if len(graphics) == 1:
    w = 0.45 if widths[0] == 1.01 else widths[0]
    figure += "\includegraphics[width=" + str(w) + "\\textwidth]{" + graphics[0] + "}\n"
    if (subCaption[0] + subLabel[0]).strip() is not "":
      figCaption.append(subCaption[0] + subLabel[0])
  else:
    linewidth = 0.
    for i, g in enumerate(graphics):
      w = 0.47
      if widths[i] != 1.01:
        w = widths[i]
      if (linewidth + w) > 1.02:
        figure += "\\\\ \n"
        linewidth = 0
      linewidth += w

      figure += "\subfloat[" + ToTeX(subCaption[i]) + "]"
      figure += "{\includegraphics[width=" + str(w) + "\\textwidth]{" + g + "}" + subLabel[i] + "}"
      figure += "\n"

  if len(figCaption) == 1:
    figure += "\caption{" + ToTeX(figCaption[0]) + "}\n"
  elif len(figCaption) > 1:
    figure += "\caption[%s]{%s}\n" % (ToTeX(figCaption[0]), ToTeX(figCaption[1]))
  figure += "\end{figure}\n\n"

  return figure

#########################################################
#########################################################

def ToTeX(line):

  line = ModifierReplacement(line)
  line = FixParentheses(line)
  line = SubsAndSupers(line)
  return SymbolReplacement(line)

#########################################################
#########################################################

# Modifiers are a bit funny -- we need to swap the order.
def ModifierReplacement(line):

  for m, v in modDict.iteritems():
    while m in line:
      pos = line.find(m)
      line = line[0:pos-1] + modDict[line[pos]] + " " + line[pos-1] + line[pos+1:]

  return line

# Get the parenthesis out of the way -- they'll mess up the sub/supers.
def FixParentheses(line):

  temp = ""
  for i in range(len(line)):
    if line[i] not in parDict or \
      (FORMAT not in ["equation", "numequation", "boxed", "align", "numalign"] and (line[:i].count("$") % 2) == 0) or \
      (line[i] in ["}", "{"] and line[i-1] != "\\") or \
      (line[i] in [")", "("] and line[i-1] == "\\"):
      temp += line[i]
    else:
      temp += parDict[line[i]]

  return temp

#########################################################
#########################################################

def SubsAndSupers(line):

  line += " "
  i = 0
  while i < len(line):
    count = 0
    if line[i] in supDict:
      count = 1
      temp = supDict[line[i]]
      while line[i+count] in supDict:
        temp += supDict[line[i+count]]
        count += 1
      temp = "^{" + temp.replace("^", "") + "} "
      line = line[0:i] + temp + line[i+count:]
    i += 1 + 2 * count
      
  i = 0
  while i < len(line):
    count = 1
    if line[i] in subDict:
      temp = subDict[line[i]]
      while line[i+count] in subDict:
        temp += subDict[line[i+count]]
        count += 1
      temp = "_{" + temp.replace("_", "") + "} "
      line = line[0:i] + temp + line[i+count:]
    i += count

  return line

#########################################################
#########################################################

def SymbolReplacement(line):

  texline = ""

  for i in range(len(line)):
    if line[i] in accDict:
      texline += accDict[line[i]]
    elif line[i] in grDict:
      texline += grDict[line[i]]
    elif line[i] in symDict:
      texline += symDict[line[i]]
    else:
      texline += line[i]

  return texline

#########################################################
#########################################################

def GetHeader(input):

  title = ""
  short_title = ""
  author = "James Saxon"
  short_author = ""
  abstract = ""
  docclass = "amsart"
  TITLE = True
  font = 11
  mT, mB, mL, mR = [1. for i in range(4)]
  header = ""

  for line in open(input):

    if line[0] is not "^":
      break

    if line[:3] == "^NT":
      TITLE = False
    if line[:3] == "^T:":
      title = ToTeX(line[3:].decode('utf-8'))
    if line[:4] == "^ST:":
      short_title = ToTeX(line[4:].decode('utf-8'))
    if line[:3] == "^A:":
      author = ToTeX(line[3:].decode('utf-8'))
    if line[:4] == "^SA:":
      short_author = ToTeX(line[4:].decode('utf-8'))
    if line[:4] == "^AB:":
      abstract = "\\begin{abstract}\n" + ToTeX(line[4:].strip().decode('utf-8')) + "\n\end{abstract}\n"
    if line[:3] == "^C:":
      docclass = line[3:].strip()
    if line[:3] == "^G:":
      geo = line[3:].strip().split()
      if len(geo) == 4:
        mT, mB, mL, mR = [float(g) for g in geo]
      elif len(geo) == 2:
        mT, mB = float(geo[0]), float(geo[0])
        mL, mR = float(geo[1]), float(geo[1])
      else:
        mT, mB, mL, mR = [float(geo[0]) for i in range(4)]
    if line[:3] == "^F:":
      font = int(line[3:].strip())
    if line[:3] == "^H:":
      header += line[3:].strip() + "\n"

  if short_title == "":
    short_title = title

  if short_author == "":
    short_author = author

  header = prologue % (font, docclass, mT, mB, mL, mR, title, author, header, short_title, title, short_author, author, abstract)
  if TITLE: header += "\n\maketitle\n\n"

  return header



#########################################################
#########################################################



def main(input, output, header, pdflatex):

  file = open(input)

  if header: header = GetHeader(input)

  document = ""

  for line in open(input):

    if line[0] == "^": continue
  
    if line == "\n":
      document += "\n"
      continue

    decline = GetSpecialFormat(line)

    # Graphics are tricky... they get pulled out.
    if max([decline.find("." + g) for g in graphs]) != -1:
      document += ProcessFigure(decline)
      continue

    if "appendix" in line: appendix = True

    texline = ToTeX(decline)

    if FORMAT: texline = TYPES[FORMAT][2] % texline.strip()

    document += texline + "\n"

  file.close()


  while "\end{itemize}\n\\begin{itemize}\n" in document or \
        "\end{enumerate}\n\\begin{enumerate}\n" in document:
    document = string.replace(document, "\end{itemize}\n\\begin{itemize}\n", "")
    document = string.replace(document, "\end{enumerate}\n\\begin{enumerate}\n", "")

  document = string.replace(document, "\end{align*}\n\\begin{align*}\n", " \\\\\n")
  document = string.replace(document, "\end{align}\n\\begin{align}\n", " \\\\\n")
  document = string.replace(document, "\end{equation}\n\\begin{equation}\n", " \\\\\n")

  if header: document = header + document + epilogue

  ofile = open(output, "w")
  ofile.write(document)
  ofile.close()

  if pdflatex: os.system('pdflatex ' + output)
  


#----------------------------------------------------
if __name__ == "__main__":

  from optparse import OptionParser

  p = OptionParser()
  p.add_option('-i', '--inputFile',  type = 'string', default = "", help = 'input File' )
  p.add_option('-o', '--outputFile', type = 'string', default = "", help = 'output File' )
  p.add_option('-d', '--header',     action = "store_true", default = False, help = 'default header and footer' )
  p.add_option('-p', '--pdflatex',   action = "store_true", default = False, help = 'run latex on the output' )

  (options,args) = p.parse_args()

  if options.inputFile == "":
    print "gotta give me a file!!"
    sys.exit()

  if options.outputFile == "":
    options.outputFile = options.inputFile + ".tex"

  main(options.inputFile, options.outputFile, options.header, options.pdflatex)


