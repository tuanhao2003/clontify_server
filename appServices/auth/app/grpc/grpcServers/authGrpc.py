import grpc
from concurrent import futures
import time
import uuid
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from protosParsed import authService_pb2, authService_pb2_grpc
from app.services.accountsService import AccountsService
from app.serializers.accountSerializer import AccountSerializer


class AuthGrpc(authService_pb2_grpc.AuthServiceServicer):
    def findByID(self, request, context):
        account = AccountsService.findByID(uuid.UUID(request.id))
        if account:
            return authService_pb2.AccountResponse(
                success=True,
                account=authService_pb2.Account(
                    id=str(account.id),
                    username=account.username,
                    email=account.email,
                    isActive=account.isActive,
                )
            )
        return authService_pb2.AccountResponse(success=False)

    def findByUsername(self, request, context):
        account = AccountsService.findByUsername(request.username)
        if account:
            return authService_pb2.AccountResponse(
                success=True,
                account=authService_pb2.Account(
                    id=str(account.id),
                    username=account.username,
                    email=account.email,
                    isActive=account.isActive,
                )
            )
        return authService_pb2.AccountResponse(success=False)

    def findByEmail(self, request, context):
        account = AccountsService.findByEmail(request.email)
        if account:
            return authService_pb2.AccountResponse(
                success=True,
                account=authService_pb2.Account(
                    id=str(account.id),
                    username=account.username,
                    email=account.email,
                    isActive=account.isActive,
                )
            )
        return authService_pb2.AccountResponse(success=False)

    def findByStatus(self, request, context):
        accounts = AccountsService.findByStatus(request.status)
        response = authService_pb2.AccountListResponse(success=True)
        if accounts:
            for acc in accounts:
                response.accounts.add(
                    id=str(acc.id),
                    username=acc.username,
                    email=acc.email,
                    isActive=acc.isActive
                )
        else:
            response.success = False
        return response

    def findByDateCreated(self, request, context):
        try:
            start = datetime.fromisoformat(request.startDate)
            end = datetime.fromisoformat(request.endDate)
            accounts = AccountsService.findByDateCreated({
                "startDate": start.isoformat(),
                "endDate": end.isoformat()
            }).data
            response = authService_pb2.AccountListResponse(success=True)
            for acc in accounts:
                response.accounts.add(
                    id=acc["id"],
                    username=acc["username"],
                    email=acc["email"],
                    isActive=acc["isActive"]
                )
            return response
        except Exception:
            return authService_pb2.AccountListResponse(success=False)

    def doCreate(self, request, context):
        data = {
            "username": request.username,
            "email": request.email,
            "password": request.password
        }
        result = AccountsService.doCreate(data)
        if result:
            return authService_pb2.OperationResponse(success=True)
        return authService_pb2.OperationResponse(success=False)

    def doUpdate(self, request, context):
        data = {
            "id": request.id,
            "email": request.email,
            "password": request.password,
            "isActive": request.isActive
        }
        result = AccountsService.doUpdate(data)
        return authService_pb2.OperationResponse(success=bool(result))

    def doDelete(self, request, context):
        result = AccountsService.doDelete(uuid.UUID(request.id))
        return authService_pb2.OperationResponse(success=result == 1)

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
