import grpc
from protosParsed import authService_pb2, authService_pb2_grpc
from app.services.accountsService import AccountsService
from app.serializers.accountSerializer import AccountSerializer
import time
from concurrent import futures
import json
import uuid

class AuthGrpc(authService_pb2_grpc.AuthServiceServicer):
    def findByID(id: str):
        return AccountsService.findByID(uuid.UUID(id))

    # def findByUsername(username: str):
    #     if not username:
    #         return -1
    #     account = AccountsRepo.getByUsername(username)
    #     if not account:
    #         return None
    #     return account

    # def findByEmail(email: str):
    #     if not email:
    #         return -1
    #     account = AccountsRepo.getByEmail(email)
    #     if not account:
    #         return None
    #     return account

    # def findByStatus(status: bool):
    #     if status is None:
    #         return -1
    #     accounts = AccountsRepo.filterByStatus(status)
    #     if not accounts:
    #         return None
    #     return accounts

    # def findByDateCreated(start: datetime, end: datetime):

    #     if not start or not end:
    #         return -1
    #     try:
    #         startDate = datetime.fromisoformat(start)
    #         endDate = datetime.fromisoformat(end)
    #     except ValueError:
    #         return -1

    #     accounts = AccountsRepo.filterByDateCreated(startDate, endDate)
    #     if not accounts or len(accounts) == 0:
    #         return None
    #     return accounts

    # def doCreate(username: str, email: str, password: str):
    #     if not username or not email or not password:
    #         return -1

    #     if AccountsRepo.getByUsername(username) or AccountsRepo.getByEmail(email):
    #         return None

    #     account = Accounts(
    #         username=username,
    #         email=email,
    #         password=make_password(password),
    #         isActive=True,
    #     )
    #     created = AccountsRepo.create(account)
    #     return created

    # def doUpdate(account: Accounts):
    #     id = account.id
    #     if not id:
    #         return -1

    #     acc = AccountsRepo.getByID(id)
    #     if not acc:
    #         return None

    #     if (account.email and AccountsRepo.getByEmail(account.email)) and (acc.email != account.email):
    #         return None

    #     acc.email = account.email or acc.email
    #     acc.password = account.password or acc.password 
    #     acc.isActive = account.isActive or acc.isActive 
    #     updated = AccountsRepo.update(acc)
    #     return updated
    
    # def doDelete(id: str):
    #     if not id:
    #         return -1
    #     deleted = AccountsRepo.delete(id)
    #     if deleted:
    #         return None
    #     return deleted

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    authService_pb2_grpc.add_AuthServiceServicer_to_server(AuthGrpc(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
