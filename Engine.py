#  Based off of pystockfish
# This handles the backend communication between our python program and any UCI engine
# It is set to use fairy stockfish to start with.

import subprocess
import Variant


class Engine(subprocess.Popen):
    """
    This initiates the Stockfish chess engine with Ponder set to False.
    'param' allows parameters to be specified by a dictionary object with 'Name' and 'value'
    with value as an integer.

    i.e. the following explicitly sets the default parameters
    {
        "Contempt Factor": 0,
        "Min Split Depth": 0,
        "Threads": 1,
        "Hash": 16,
        "MultiPV": 1,
        "Skill Level": 20,
        "Move Overhead": 30,
        "Minimum Thinking Time": 20,
        "Slow Mover": 80,
    }

    If 'rand' is set to False, any options not explicitly set will be set to the default
    value.

    -----
    USING RANDOM PARAMETERS
    -----
    If you set 'rand' to True, the 'Contempt' parameter will be set to a random value between
    'rand_min' and 'rand_max' so that you may run automated matches against slightly different
    engines.
    """

    def __init__(self, depth=2, param={}, args=("fairy-stockfish_x86-64.exe")):
        """

        :param depth: The depth to which the engine will think each move. Default is 2.
        :param param: A dictionary of UCI values to send to the engine upon the initialization of this class.
        :param args: A tuple containing the command to start the engine, followed by any CLAs
        """
        subprocess.Popen.__init__(self,
                                  args,
                                  universal_newlines=True,
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE, )
        # ("fairy-stockfish_x86-64.exe", "load", "variants.ini")
        self.depth = str(depth)
        self.put('uci')
        self.variant: Variant = Variant.StaticVariants.CHESS

        base_param = {
            "Write Debug Log": "false",
            "Contempt Factor": 0,  # There are some stockfish versions with Contempt Factor
            "Contempt": 0,  # and others with Contempt. Just try both.
            "Min Split Depth": 0,
            "Threads": 1,
            "Hash": 16,
            "MultiPV": 1,
            "Skill Level": 20,
            "Move Overhead": 30,
            "Minimum Thinking Time": 20,
            "Slow Mover": 80,
            "UCI_Chess960": "false",
            "Ponder": False,
        }

        #if rand:
        #    base_param['Contempt'] = randint(rand_min, rand_max),
        #    base_param['Contempt Factor'] = randint(rand_min, rand_max),

        base_param.update(param)
        self.param = base_param
        for name, value in list(base_param.items()):
            self.setoption(name, value)

    def newgame(self):
        """
        Calls 'ucinewgame' - this should be run before a new game
        """
        self.put('ucinewgame')
        self.isready()

    def put(self, command):
        # print(command)
        self.stdin.write(command + '\n')
        self.stdin.flush()

    def flush(self):
        self.stdout.flush()

    def setoption(self, optionname, value):
        self.put('setoption name %s value %s' % (optionname, str(value)))
        stdout = self.isready()
        if stdout.find('No such') >= 0:
            print("stockfish was unable to set option %s" % optionname)

    def setVariant(self, variant:Variant, variantPath=None):
        """
        Changes the variant that this engine is playing.
        :param variant: The variant that we want to set this engine to
        :return:none
        """
        self.variant = variant

        if variantPath is not None and not variant.builtIn:
            self.setoption("VariantPath", variantPath)
        self.setoption("UCI_Variant", variant.name)

    def setposition(self, moves=()):
        """
        Move list is a list of moves (i.e. ['e2e4', 'e7e5', ...]) each entry as a string.  Moves must be in full algebraic notation.
        """
        self.put('position fen {0} moves {1}'.format(self.variant.startingFEN, self._movelisttostr(moves)))
        # self.put('position startpos moves %s' % self._movelisttostr(moves))
        self.isready()

    def setfenposition(self, fen):
        """
        set position in fen notation.  Input is a FEN string i.e. "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
        """
        self.put('position fen %s' % fen)
        self.isready()

    def go(self):
        self.put('go depth %s' % self.depth)

    def _movelisttostr(self, moves):
        """
        Concatenates a list of strings
        """
        movestr = ''
        for h in moves:
            movestr += h + ' '
        return movestr.strip()

    def bestmove(self) -> dict:
        """

        :return: A dictionary with three K,V pairs:
        'move', and the best move,
        'ponder' and any ponder move,
        'info' and the line of info that stockfish gives
        Additionally, if mate is found, then it will include the pair
        'mate' and the number of moves till mate (sign indicates which engine has mate. >0 for this engine, <0 for the other engine)
        """
        last_line = ""
        self.go()
        while True:
            text = self.stdout.readline().strip()
            split_text = text.split(' ')
            if split_text[0] == 'bestmove':
                moveInfo = {'move': split_text[1],
                        'ponder': split_text[3] if len(split_text) > 2 else "(none)", # Added by Eli to fix bug
                        'info': last_line}
                mateloc = last_line.find('mate')
                if mateloc >= 0:
                    # print(last_line)
                    endofcountloc = last_line.find(" ", mateloc + 5)

                    matenum = int(last_line[mateloc + 5:endofcountloc] if endofcountloc >= 0 else last_line[mateloc + 5])
                    moveInfo['mate'] = matenum

                return moveInfo
            last_line = text

    def isready(self):
        """
        Used to synchronize the python engine object with the back-end engine.  Sends 'isready' and waits for 'readyok.'
        """
        self.put('isready')
        retryCount: int = 20
        while retryCount > 0:
            text = self.stdout.readline().strip()
            # print("Waiting: {0}".format(text))
            if text == 'readyok':
                return text
            elif text == '':
                retryCount -= 1
            else:
                retryCount = 20
        raise ConnectionAbortedError("Engine did not return isready!")
