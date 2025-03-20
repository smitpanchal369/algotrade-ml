from enum import Enum
from dataclasses import dataclass


class ExchSeg(Enum):
    BFO = "BFO"
    BSE = "BSE"
    CDS = "CDS"
    MCX = "MCX"
    NCDEX = "NCDEX"
    NCO = "NCO"
    NFO = "NFO"
    NSE = "NSE"


class Instrumenttype(Enum):
    AMXIDX = "AMXIDX"
    COMDTY = "COMDTY"
    EMPTY = ""
    FUTBAS = "FUTBAS"
    FUTBLN = "FUTBLN"
    FUTCOM = "FUTCOM"
    FUTCUR = "FUTCUR"
    FUTENR = "FUTENR"
    FUTIDX = "FUTIDX"
    FUTIRC = "FUTIRC"
    FUTIRT = "FUTIRT"
    FUTSTK = "FUTSTK"
    INDEX = "INDEX"
    OPTBLN = "OPTBLN"
    OPTCUR = "OPTCUR"
    OPTFUT = "OPTFUT"
    OPTIDX = "OPTIDX"
    OPTIRC = "OPTIRC"
    OPTSTK = "OPTSTK"
    UNDCUR = "UNDCUR"
    UNDIRC = "UNDIRC"
    UNDIRD = "UNDIRD"
    UNDIRT = "UNDIRT"


@dataclass
class ScripMaster:
    token: str
    symbol: str
    name: str
    expiry: str
    strike: str
    lotsize: str
    instrumenttype: Instrumenttype
    exch_seg: ExchSeg
    tick_size: str
