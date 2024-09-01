import pytest
from unittest.mock import MagicMock
from src.services.batch_service import BatchService
from src.tasks import process_batch_message

class MockBatch:
    def __init__(self, batch_id, created_at, id, piglet_count, status, updated_at):
        self.batch_id = batch_id
        self.created_at = created_at
        self.id = id
        self.piglet_count = piglet_count
        self.status = status
        self.updated_at = updated_at

    def to_dict(self):
        return {
            "batch_id": self.batch_id,
            "created_at": self.created_at,
            "id": self.id,
            "piglet_count": self.piglet_count,
            "status": self.status,
            "updated_at": self.updated_at,
        }


@pytest.fixture
def batch_repository_mock():
    return MagicMock()


@pytest.fixture
def batch_service(batch_repository_mock):
    return BatchService(batch_repository=batch_repository_mock)

@pytest.fixture
def app(app):
    return app

def test_create_batch_missing_parameters(batch_service):

    response, status_code = batch_service.create_batch(None, 'created', 25)
    assert response == {"message": "Missing required parameters"}
    assert status_code == 400

    response, status_code = batch_service.create_batch('1', None, 25)
    assert response == {"message": "Missing required parameters"}
    assert status_code == 400

    response, status_code = batch_service.create_batch('1', 'created', None)
    assert response == {"message": "Missing required parameters"}
    assert status_code == 400

def test_create_batch_creation_failed(batch_service, mocker):
  
    batch_repository_mock = batch_service.batch_repository
    batch_repository_mock.create_batch.return_value = None

    mocker.patch('src.tasks.process_batch_message.apply_async')  

    response, status_code = batch_service.create_batch('1', 'created', 25)
    assert response == {"message": "Batch creation failed"}
    assert status_code == 500

    batch_repository_mock.create_batch.assert_called_once_with(
        batch_id='1', status='created', piglet_count=25
    )
    process_batch_message.apply_async.assert_not_called()

def test_create_batch_success(batch_service, mocker):

    mock_batch = MagicMock()
    mock_batch.to_dict.return_value = {
        'batch_id': '1',
        'status': 'created',
        'piglet_count': 25
    }
    batch_service.batch_repository.create_batch.return_value = mock_batch

    mocker.patch('src.tasks.process_batch_message.apply_async') 

    response, status_code = batch_service.create_batch('1', 'created', 25)
    assert response == {
        'batch_id': '1',
        'status': 'created',
        'piglet_count': 25
    }
    assert status_code == 201

    batch_service.batch_repository.create_batch.assert_called_once_with(
        batch_id='1', status='created', piglet_count=25
    )
    process_batch_message.apply_async.assert_called_once_with(
        args=[{
            "action": "create",
            "batch_id": '1',
            "status": 'created',
            "piglet_count": 25,
        }]
    )

def test_list_all_batches_by_status(batch_service, batch_repository_mock):

    mock_batches = [MockBatch("1", "2024-08-30", 49, 25, "created", "2024-08-30")]
    batch_repository_mock.list_all_batches_by_status.return_value = mock_batches

    status = "created"
    result, status_code = batch_service.list_all_batches_by_status(status)

    batch_repository_mock.list_all_batches_by_status.assert_called_once_with(status)

  
    expected_result = [
        {
            "batch_id": "1",
            "created_at": "2024-08-30",
            "id": 49,
            "piglet_count": 25,
            "status": "created",
            "updated_at": "2024-08-30",
        }
    ]

    assert result == expected_result
    assert status_code == 200

def test_list_all_batches_empty(batch_service, app):

    batch_repository_mock = batch_service.batch_repository
    batch_repository_mock.list_all_batches.return_value = []

    with app.app_context(): 
        response, status_code = batch_service.list_all_batches()

    assert response.json == []
    assert status_code == 200

def test_list_all_batches_with_data(batch_service, app):

    mock_batches = [
        MockBatch("1", "2024-08-30", 49, 25, "created", "2024-08-30"),
        MockBatch("2", "2024-08-31", 50, 30, "updated", "2024-08-31")
    ]
    batch_repository_mock = batch_service.batch_repository
    batch_repository_mock.list_all_batches.return_value = mock_batches

    with app.app_context():
        response, status_code = batch_service.list_all_batches()

    expected_result = [
        {
            'batch_id': "1",
            'created_at': "2024-08-30",
            'id': 49,
            'piglet_count': 25,
            'status': "created",
            'updated_at': "2024-08-30"
        },
        {
            'batch_id': "2",
            'created_at': "2024-08-31",
            'id': 50,
            'piglet_count': 30,
            'status': "updated",
            'updated_at': "2024-08-31"
        }
    ]

    assert response.json == expected_result
    assert status_code == 200
    
def test_update_batch_missing_parameters(batch_service):

    response, status_code = batch_service.update_batch(None, 25)
    assert response == {"message": "Missing required parameters"}
    assert status_code == 400

    response, status_code = batch_service.update_batch('1', None)
    assert response == {"message": "Missing required parameters"}
    assert status_code == 400

def test_update_batch_not_found(batch_service, mocker):
 
    batch_repository_mock = batch_service.batch_repository
    batch_repository_mock.update_batch.return_value = None

    mocker.patch('src.tasks.process_batch_message.apply_async')  

    response, status_code = batch_service.update_batch('1', 25)
    assert response == {"message": "Batch not found"}
    assert status_code == 404

    batch_repository_mock.update_batch.assert_called_once_with('1', 25)
    process_batch_message.apply_async.assert_not_called()

def test_update_batch_success(batch_service, mocker):

    batch_repository_mock = batch_service.batch_repository
    batch_repository_mock.update_batch.return_value = True  

    mocker.patch('src.tasks.process_batch_message.apply_async') 

    response, status_code = batch_service.update_batch('1', 25)
    assert response == {"message": "Batch updated successfully!"}
    assert status_code == 200

    batch_repository_mock.update_batch.assert_called_once_with('1', 25)
    process_batch_message.apply_async.assert_called_once_with(
        args=[{
            "action": "update",
            "batch_id": '1',
            "piglet_count": 25,
        }]
    )

def test_delete_batch_not_found(batch_service, mocker):

    batch_repository_mock = batch_service.batch_repository
    batch_repository_mock.delete_batch.return_value = None

    mocker.patch('src.tasks.process_batch_message.apply_async')  

    response, status_code = batch_service.delete_batch('1')
    assert response == {"message": "Batch not found"}
    assert status_code == 404

    batch_repository_mock.delete_batch.assert_called_once_with('1')
    process_batch_message.apply_async.assert_not_called()

def test_delete_batch_success(batch_service, mocker):
   
    batch_repository_mock = batch_service.batch_repository
    batch_repository_mock.delete_batch.return_value = True  

    mocker.patch('src.tasks.process_batch_message.apply_async')  

    response, status_code = batch_service.delete_batch('1')
    assert response == {"message": "Batch deleted successfully!"}
    assert status_code == 200

    batch_repository_mock.delete_batch.assert_called_once_with('1')
    process_batch_message.apply_async.assert_called_once_with(
        args=[{
            "action": "delete",
            "batch_id": '1',
        }]
    )  