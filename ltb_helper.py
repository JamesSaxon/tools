#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

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
  "⇒".decode('utf-8'): "\\thus ", 
  "⟹".decode('utf-8'): "\\thus ", 
  "∫".decode('utf-8'): "\int ", 
  "∮".decode('utf-8'): "\oint ", 
  "·".decode('utf-8'): "\cdot ", 
  "±".decode('utf-8'): "\pm ", 
  "∓".decode('utf-8'): "\mp ", 
  "✔".decode('utf-8'): "\cmark ", 
  "✘".decode('utf-8'): "\\xmark ", 
  "○".decode('utf-8'): "\pie{0}  {red} ", 
  "◔".decode('utf-8'): "\pie{90} {red} ", 
  "◑".decode('utf-8'): "\pie{180}{red} ", 
  "◕".decode('utf-8'): "\pie{270}{darkgreen} ", 
  "●".decode('utf-8'): "\pie{360}{darkgreen} ", 
  "°".decode('utf-8'): "\degree", 
  "≈".decode('utf-8'): "\\approx ", 
  "≡".decode('utf-8'): "\equiv ", 
  "∝".decode('utf-8'): "\propto ", 
  "∈".decode('utf-8'): "\in ", 
  "≠".decode('utf-8'): "\\neq ", 
  "∞".decode('utf-8'): "\infty ", 
  "√".decode('utf-8'): "\sqrt ", 
  "ħ".decode('utf-8'): "\hbar ", 
  "∇".decode('utf-8'): "\\nabla ", 
  "Ɇ".decode('utf-8'): "\slashed{E}", 
  "ℋ".decode('utf-8'): "\mathcal{H} ", 
  "ℒ".decode('utf-8'): "\mathcal{L} ", 
  "𝒪".decode('utf-8'): "\mathcal{O} ", 
  "∂".decode('utf-8'): "\partial ", 
  "ℓ".decode('utf-8'): "\ell ",
  "÷".decode('utf-8'): "\\frac",
  "☺".decode('utf-8'): "\smiley{}",
  "║".decode('utf-8'): "\parallel",
  "┴".decode('utf-8'): "\\bot",
  "¡".decode('utf-8'): "\\text{<}",
  "¿".decode('utf-8'): "\\text{>}",
  "§".decode('utf-8'): "\S{}",
  "“".decode('utf-8'): "``",
  "”".decode('utf-8'): '"',
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
#  "*".decode('utf-8'): "^\star ",
  "⁺".decode('utf-8'): "^+ ",
  "⁻".decode('utf-8'): "^- ",
  "ᵀ".decode('utf-8'): "^T ",
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
  "ᵢ".decode('utf-8'): "_i ",
  "ⱼ".decode('utf-8'): "_j ",
}

accDict = {
  "á".decode('utf-8'): "\\'a",
  "à".decode('utf-8'): "\`a",
  "é".decode('utf-8'): "\\'e",
  "è".decode('utf-8'): "\`e",
  "ï".decode('utf-8'): "\\\"i",
  "ü".decode('utf-8'): "\\\"u",
  "ä".decode('utf-8'): "\\\"a",
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

#########################################################
#########################################################

def ToTeX(line):

  line = ModifiersAndParentheses(line)
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

#def FixParentheses(line):
#  # Aside that, get the parenthesis out of the way -- they'll mess up the sub/supers.
#  temp = ""
#  for i in range(len(line)):
#    if line[i] not in parDict or \
#      (FORMAT is not TYPES.index("equation") and FORMAT is not TYPES.index("numequation") and FORMAT is not TYPES.index("boxed") and FORMAT is not TYPES.index("align") and FORMAT is not TYPES.index("numalign") and (line[:i].count("$") % 2) == 0) or \
#      (line[i] in ["}", "{"] and line[i-1] != "\\") or \
#      (line[i] in [")", "("] and line[i-1] == "\\"):
#      temp += line[i]
#    else:
#      temp += parDict[line[i]]
#
#  return temp

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

  line = SubsAndSupers(line)

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

  return texline.strip()




