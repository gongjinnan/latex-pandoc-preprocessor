"""
Holds the PreProcess class. This class contains functions that populate the

    PreProcess.ParsedData

dictionary - this contains the objects defined in types.py and parses the data.

It takes in the initial .tex string, replaces with uids and leaves you with
the above array and PreeProcess.ParsedText which should be written to a
temporary file and ran through pandoc to markdown.

It also contains the PostProcess class. This should be given the markdown
string so that it can replace the unique ids generated by PreProcess with
the generated text.

Extract the final string with:

    PostProcess.ParsedText

Author: Josh Borrow
Date Created: 2016-09-09.
"""

import random
import re
import copy
import string
from ltmd.parsetypes import *


class PreProcess(object):
    def __init__(self, InputText, ImgPrepend=""):
        self.InputText = InputText
        self.ParsedText = copy.deepcopy(self.InputText)
        self.ImgPrepend = ImgPrepend
        self.ParsedRef = {}
        self.ParsedCite = {}
        self.ParsedMath = {}
        self.ParsedFig = {}
        self.ParsedWrapFig = {}
        
        self.RefExtract()
        self.ReplaceAll(self.ParsedRef)

        self.CiteExtract()
        self.ReplaceAll(self.ParsedCite)

        self.MathExtract()
        self.ReplaceAll(self.ParsedMath)

        self.WrapFigExtract()
        self.ReplaceAll(self.ParsedWrapFig)

        self.FigExtract()
        self.ReplaceAll(self.ParsedFig)

        self.ParsedData = {
                'ref': self.ParsedRef,
                'cite': self.ParsedCite,
                'math': self.ParsedMath,
                'fig': self.ParsedFig,
                'wfig': self.ParsedWrapFig,
        }


    def GenerateUID(self):
        r""" Generates a Unique Identifier - checks if it is already in
        self.ParsedData.keys() - if not it gets returned for use elsewhere."""

        UID = random.randint(0, 1e10)

        return "{:0>10}".format(UID)


    def RefExtract(self):
        r""" Finds all references in the text, generates UIDs and places
        the text in a Ref instance. """
        Regex = r"\\ref\{.*?\}"
        self.RefRegex = re.compile(Regex, re.VERBOSE|re.DOTALL)

        RefExtracted = self.RefRegex.findall(self.ParsedText)

        for Reference in RefExtracted:
            ThisUID = self.GenerateUID()
            self.ParsedRef[ThisUID] = Ref(Reference, ThisUID)

    
    def CiteExtract(self):
        r""" Finds all cites in the text. This is a passthrough. """
        
        Regex = r"\\cite\{.*?\}"
        self.CiteRegex = re.compile(Regex, re.VERBOSE|re.DOTALL)

        CiteExtracted = self.CiteRegex.findall(self.ParsedText)

        for Citation in CiteExtracted:
            ThisUID = self.GenerateUID()
            self.ParsedCite[ThisUID] = Cite(Citation, ThisUID)


    def MathExtract(self):
        r""" Finds all equations in the text, generates UIDs and places
        the text in a Math instance. """

        Regex = r"\\begin\{equation\}.*?\\end\{equation\}"
        self.MathRegex = re.compile(Regex, re.VERBOSE|re.DOTALL)

        MathExtracted = self.MathRegex.findall(self.ParsedText)

        for Mathematics in MathExtracted:
            ThisUID = self.GenerateUID()
            self.ParsedMath[ThisUID] = Math(Mathematics, ThisUID)


    def FigExtract(self):
        r""" Finds all figures in the text, generates UIDs and places
        the text in a Fig instance. """

        Regex = r"\\begin\{figure\}.*?\\end\{figure\}"
        self.FigRegex = re.compile(Regex, re.VERBOSE|re.DOTALL)

        FigExtracted = self.FigRegex.findall(self.ParsedText)

        for FigureText in FigExtracted:
            ThisUID = self.GenerateUID()
            self.ParsedFig[ThisUID] = Figure(FigureText, ThisUID, self.ImgPrepend)


    def WrapFigExtract(self):
        r""" Same as above but looks for wrapfigures """

        Regex = r"\\begin\{wrapfigure\}.*?\\end\{wrapfigure\}"
        self.WrapFigRegex = re.compile(Regex, re.VERBOSE|re.DOTALL)

        FigExtracted = self.WrapFigRegex.findall(self.ParsedText)

        for FigureText in FigExtracted:
            ThisUID = self.GenerateUID()
            self.ParsedWrapFig[ThisUID] = Figure(FigureText, ThisUID, self.ImgPrepend)


    def ReplaceAll(self, toParse):
        """ Replaces all of the OriginalContent from the objects in ParsedData
        with their respective Unique Identifiers. """

        for UID, Instance in toParse.items():
            self.ParsedText = self.ParsedText.replace(Instance.OriginalContent, UID)


class PostProcess(object):
    def __init__(self, InputText, ParsedData):
        self.InputText = InputText
        self.ParsedText = copy.deepcopy(self.InputText)

        self.ReplaceAll(ParsedData['wfig'])
        self.ReplaceAll(ParsedData['fig'])
        self.ReplaceAll(ParsedData['math'])
        self.ReplaceAll(ParsedData['cite'])
        self.ReplaceAll(ParsedData['ref'])
    
    def ReplaceAll(self, toParse):
        """ Replaces all of the Unique Identifiers from ParsedData with their
        markdown-ified expressions from ParsedData. """
       
        for UID, Instance in toParse.items():
            self.ParsedText = self.ParsedText.replace(UID, Instance.OutputContent)

