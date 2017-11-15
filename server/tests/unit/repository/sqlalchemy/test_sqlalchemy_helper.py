from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
import pytest

from app.repository.sqlalchemy.sqlalchemy_helper import choose_columns


class TestChooseColumns(object):
    @pytest.fixture
    def table(self):
        metadata = MetaData()
        table = Table('table1', metadata,
                      Column('field1', Integer, primary_key=True),
                      Column('field2', String(50), nullable=False))
        engine = create_engine('sqlite:///:memory:')
        metadata.create_all(engine)
        yield table
        metadata.drop_all(engine)

    def test_choose_one_column(self, table):
        columns = choose_columns(table, 'field1')
        assert len(columns) == 1
        assert isinstance(columns[0], Column)
        assert columns[0].name == 'field1'

    def test_choose_multiple_columns(self, table):
        columns = choose_columns(table, 'field1', 'field2')
        assert len(columns) == 2
        assert columns[0].name == 'field1'
        assert columns[1].name == 'field2'

    def test_alias_column(self, table):
        columns = choose_columns(table, ('field1', 'alias1'),
                                 ('field2', 'alias2'))
        assert columns[0].name == 'alias1'
        assert columns[1].name == 'alias2'
