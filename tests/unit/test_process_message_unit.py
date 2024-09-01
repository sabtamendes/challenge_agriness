import pytest
from unittest.mock import patch, MagicMock
from src.tasks import process_batch_message

@pytest.fixture
def mock_batch_repository():
    return MagicMock()

@pytest.fixture
def mock_update_key():
    with patch('src.tasks.update_key') as mock:
        yield mock

@pytest.fixture
def mock_delete_key():
    with patch('src.tasks.delete_key') as mock:
        yield mock

@pytest.fixture
def app_context():
    with patch('src.main.create_app') as mock_create_app:
        mock_app = MagicMock()
        mock_create_app.return_value = mock_app
        mock_app.app_context.return_value.__enter__.return_value = mock_app
        yield mock_app

def test_process_batch_message_create(app_context, mock_batch_repository, mock_update_key):
    with patch('src.tasks.BatchRepository', return_value=mock_batch_repository):
        message = {
            'action': 'create',
            'batch_id': '1',
            'status': 'created',
            'piglet_count': 25
        }
        
        process_batch_message(message)

        mock_batch_repository.create_batch.assert_called_once_with('1', 'created', 25)
        mock_update_key.assert_called_once_with('1', 25)

def test_process_batch_message_update(app_context, mock_batch_repository, mock_update_key):
    with patch('src.tasks.BatchRepository', return_value=mock_batch_repository):
        message = {
            'action': 'update',
            'batch_id': '1',
            'piglet_count': 30
        }
        
        process_batch_message(message)

        mock_batch_repository.update_batch.assert_called_once_with('1', 30)
        mock_update_key.assert_called_once_with('1', 30)

def test_process_batch_message_delete(app_context, mock_batch_repository, mock_delete_key):
    with patch('src.tasks.BatchRepository', return_value=mock_batch_repository):
        message = {
            'action': 'delete',
            'batch_id': '1'
        }
        
        process_batch_message(message)

        mock_batch_repository.delete_batch.assert_called_once_with('1')
        mock_delete_key.assert_called_once_with('1')

def test_process_batch_message_unknown_action(app_context):
    with patch('src.tasks.BatchRepository') as mock_batch_repository:
        message = {
            'action': 'unknown',
            'batch_id': '1'
        }
        
        with pytest.raises(ValueError, match="Unknown message action"):
            process_batch_message(message)
