from abc import ABCMeta, abstractmethod
from unittest import TestCase
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData

from app.repos import choose_columns


class MockDbEnvironmentTestCase(TestCase, metaclass=ABCMeta):
    @abstractmethod
    def mock_tables(self, metadata):
        pass

    def setUp(self):
        self.metadata = MetaData()
        for table_name, table in self.mock_tables(self.metadata).items():
            setattr(self, table_name, table)
        self.engine = create_engine('sqlite:///:memory:')
        self.metadata.create_all(self.engine)

    def tearDown(self):
        self.metadata.drop_all(self.engine)


class ColumnChooserTestCase(MockDbEnvironmentTestCase):
    def mock_tables(self, metadata):
        return {'table1': Table('table1', metadata,
                                Column('field1', Integer, primary_key=True),
                                Column('field2', String(50), nullable=False))}

    def test_choose_one_column(self):
        columns = choose_columns(self.table1, 'field1')
        self.assertEqual(len(columns), 1)
        self.assertTrue(isinstance(columns[0], Column))
        self.assertEqual(columns[0].name, 'field1')

    def test_choose_multiple_columns(self):
        columns = choose_columns(self.table1, 'field1', 'field2')
        self.assertEqual(len(columns), 2)
        self.assertEqual(columns[0].name, 'field1')
        self.assertEqual(columns[1].name, 'field2')

    def test_alias_column(self):
        columns = choose_columns(self.table1, ('field1', 'alias1'),
                                 ('field2', 'alias2'))
        self.assertEqual(columns[0].name, 'alias1')
        self.assertEqual(columns[1].name, 'alias2')
