
validOrientations = ("0", "90", "180", "270")

def getPieceDefinition(piece, char:str) -> str:
    """

    This function returns the command for the LaTeX package chessboard to define the look of this piece.

    The specific command is \cbReDefineNewPiece.

    :param piece: The piece for which we want the definition
    :return: A string containing the definition of this piece.
    """

    # 0: Color (all lowercase)
    # 1: Char
    # 2: Color (first letter uppercase)
    # 3: Base piece name (first letter uppecase)
    # 4: Orientation Modifier
    # 5: Orientation Modifier closing braces
    command = r"\cbReDefineNewPiece{{{0}}}{{{1}}}{{\raisebox{{\depth}}{{{4}\cfss@{0}piececolor\cfss@{2}{3}OnWhite{5}}}}}{{\raisebox{{\depth}}{{{4}\cfss@{2}{3}OnBlack{5}}}}}"

    out = ""

    # This contains the LaTeX commands to rotate the piece.
    # We flip the piece at 90 and 270 to ensure the background lines on the black squares are consistent.
    orientations = {
        "0":("", ""),
        "90":(r"\rotatebox[origin=c]{90}{\scalebox{1}[-1]{","}}"),
        "180":(r"\rotatebox[origin=c]{180}{","}"),
        "270":(r"\rotatebox[origin=c]{270}{\scalebox{1}[-1]{","}}"),
    }

    orientation = piece.latexOrientation
    basePiece = piece.latexBase

    ori, oriClose = orientations[orientation]

    for color, Color, upper in (("white", "White", True), ("black", "Black", False)):
        out += command.format(color, char.upper() if upper else char.lower(), Color, basePiece, ori, oriClose)

    return "\makeatletter\n{0}\n\makeatother".format(out)


def getMatchLatex(match) -> str:
    """
    This function turns a match into a LaTeX string, so that we can look at it with our glorious eyeballs.
    :param match: The match that we want the LaTeX source of
    :return: A string containing the latex source of that match
    """

    variant = match.variant

    pieceDefinitions = "\n".join(getPieceDefinition(piece, char) for char, piece in variant.getVariantMen().items())

    header = "\section{{{0} Match {1}: {2}}}".format(variant.name, match.round, match.result)

    game = "\n".join("\chessboard[setfen={0}]".format(FEN) for FEN in match.FEN)

    return "{0}\n{1}\n{2}".format(pieceDefinitions, header, game)


