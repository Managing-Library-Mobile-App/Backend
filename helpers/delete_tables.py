from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Inspector, MetaData
from sqlalchemy.sql.ddl import DropConstraint, DropTable


def delete_tables(db: SQLAlchemy, tables_to_not_delete: list[str] = None):
    con = db.engine.connect()
    trans = con.begin()
    inspector = Inspector.from_engine(db.engine)
    meta = MetaData()
    tables = []
    all_fkeys = []
    for table_name in inspector.get_table_names():
        if tables_to_not_delete:
            if table_name in tables_to_not_delete:
                continue
        fkeys = []
        for fkey in inspector.get_foreign_keys(table_name):
            if not fkey["name"]:
                continue
            fkeys.append(db.ForeignKeyConstraint((), (), name=fkey["name"]))
        tables.append(Table(table_name, meta, *fkeys))
        all_fkeys.extend(fkeys)
    for fkey in all_fkeys:
        con.execute(DropConstraint(fkey))
    for table in tables:
        con.execute(DropTable(table))
    trans.commit()
    db.create_all()
