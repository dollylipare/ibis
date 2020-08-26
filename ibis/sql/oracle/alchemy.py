from sqlalchemy.dialects.oracle.base import OracleDialect
import sqlalchemy as sa
import ibis.sql.oracle.expr.datatypes as dt
import ibis.sql.alchemy as s_al


geospatial_supported = False
try:
    import geoalchemy2 as ga
    import geoalchemy2.shape as shape
    import geopandas

    geospatial_supported = True
except ImportError:
    pass

_ibis_type_to_sqla = {
    dt.CLOB: sa.CLOB,
    #dt.NCLOB: sa.NCLOB,
    #dt.LONG: sa.LONG,
    #dt.NUMBER: sa.NUMBER,
    #dt.BFILE: sa.BFILE,
    #dt.RAW: sa.RAW,
    dt.LONGRAW: sa.Binary,
}
_ibis_type_to_sqla.update(s_al._ibis_type_to_sqla)

def _to_sqla_type(itype, type_map=None):
    if type_map is None:
        type_map = _ibis_type_to_sqla
    if isinstance(itype, dt.Decimal):
        return sa.types.NUMERIC(itype.precision, itype.scale)
    elif isinstance(itype, dt.Date):
        return sa.Date()
    elif isinstance(itype, dt.Timestamp):
        # SQLAlchemy DateTimes do not store the timezone, just whether the db
        # supports timezones.
        return sa.TIMESTAMP(bool(itype.timezone))
    elif isinstance(itype, dt.Array):
        ibis_type = itype.value_type
        if not isinstance(ibis_type, (dt.Primitive, dt.String)):
            raise TypeError(
                'Type {} is not a primitive type or string type'.format(
                    ibis_type
                )
            )
        return sa.ARRAY(_to_sqla_type(ibis_type, type_map=type_map))
    elif geospatial_supported and isinstance(itype, dt.GeoSpatial):
        if itype.geotype == 'geometry':
            return ga.Geometry
        elif itype.geotype == 'geography':
            return ga.Geography
        else:
            return ga.types._GISType
    else:
        return type_map[type(itype)]

class AlchemyExprTranslator(s_al.AlchemyExprTranslator):
    s_al.AlchemyExprTranslator._type_map = _ibis_type_to_sqla

class AlchemyDialect(s_al.AlchemyDialect):
    s_al.translator = AlchemyExprTranslator

@dt.dtype.register(OracleDialect, sa.dialects.oracle.CLOB)
def sa_oracle_CLOB(_, satype, nullable=True):
    return dt.CLOB(nullable=nullable)


@dt.dtype.register(OracleDialect, sa.dialects.oracle.NCLOB)
def sa_oracle_NCLOB(_, satype, nullable=True):
    return dt.NCLOB(nullable=nullable)


@dt.dtype.register(OracleDialect, sa.dialects.oracle.LONG)
def sa_oracle_LONG(_, satype, nullable=True):
    return dt.LONG(nullable=nullable)


@dt.dtype.register(OracleDialect, sa.dialects.oracle.NUMBER)
def sa_oracle_NUMBER(_, satype, nullable=True):
    return dt.Number(satype.precision, satype.scale, nullable=nullable)


@dt.dtype.register(OracleDialect, sa.dialects.oracle.BFILE)
def sa_oracle_BFILE(_, satype, nullable=True):
    return dt.BFILE(nullable=nullable)


@dt.dtype.register(OracleDialect, sa.dialects.oracle.RAW)
def sa_oracle_RAW(_, satype, nullable=True):
    return dt.RAW(nullable=nullable)


@dt.dtype.register(OracleDialect, sa.types.BINARY)
def sa_oracle_LONGRAW(_, satype, nullable=True):
    return dt.LONGRAW(nullable=nullable)
