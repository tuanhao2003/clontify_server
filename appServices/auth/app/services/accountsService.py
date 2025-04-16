from app.repositories.accountsRepo import AccountsRepo
from datetime import datetime
from app.entities.accounts import Accounts
from common.baseResponse import BaseResponse
from app.serializers.accountSerializer import AccountSerializer


class AccountsService:
    @staticmethod
    def findByID(data: dict):
        id = data.get("id")
        if not id:
            return BaseResponse.badRequest("Dữ liệu không hợp lệ")
        account = AccountsRepo.getByID(id)
        if not account:
            return BaseResponse.notFound("Không tìm thấy tài khoản")
        return BaseResponse.success(data=AccountSerializer(account).data)

    @staticmethod
    def findByUsername(data: dict):
        username = data.get("username")
        if not username:
            return BaseResponse.badRequest("Dữ liệu không hợp lệ")
        account = AccountsRepo.getByUsername(username)
        if not account:
            return BaseResponse.notFound("Không tìm thấy tài khoản")
        return BaseResponse.success(data=AccountSerializer(account).data)

    @staticmethod
    def findByEmail(data: dict):
        email = data.get("email")
        if not email:
            return BaseResponse.badRequest("Dữ liệu không hợp lệ")
        account = AccountsRepo.getByEmail(email)
        if not account:
            return BaseResponse.notFound("Không tìm thấy tài khoản")
        return BaseResponse.success(data=AccountSerializer(account).data)

    @staticmethod
    def findByStatus(data: dict):
        status = data.get("isActive")
        if status is None:
            return BaseResponse.badRequest("Dữ liệu không hợp lệ")
        accounts = AccountsRepo.filterByStatus(status)
        if not accounts:
            return BaseResponse.notFound("Không có tài khoản phù hợp")
        serialized = AccountSerializer(accounts, many=True).data
        return BaseResponse.success(data=serialized)

    @staticmethod
    def findByDateCreated(data: dict):
        start = data.get("start")
        end = data.get("end")

        if not start or not end:
            return BaseResponse.badRequest(
                "Dữ liệu không hợp lệ"
            )

        try:
            startDate = datetime.fromisoformat(start)
            endDate = datetime.fromisoformat(end)
        except ValueError:
            return BaseResponse.badRequest(
                "Sai định dạng"
            )

        accounts = AccountsRepo.filterByDateCreated(startDate, endDate)
        if not accounts or len(accounts) == 0:
            return BaseResponse.notFound(
                "Không có tài khoản nào được tạo trong khoảng thời gian này"
            )

        accountToJSON = AccountSerializer(accounts, many=True).data
        return BaseResponse.success(data=accountToJSON)

    @staticmethod
    def doCreate(data: dict):
        requiredFields = ["username", "email", "password"]
        for field in requiredFields:
            if not data.get(field):
                return BaseResponse.badRequest(f"{field} không được để trống")

        if AccountsRepo.getByUsername(data["username"]) or AccountsRepo.getByEmail(
            data["email"]
        ):
            return BaseResponse.conflict("Tài khoản đã tồn tại")

        account = Accounts(
            username=data["username"],
            email=data["email"],
            password=data["password"],
            isActive=True,
        )
        created = AccountsRepo.create(account)
        return BaseResponse.success(
            "Tạo tài khoản thành công", AccountSerializer(created).data
        )

    @staticmethod
    def doUpdate(data: dict):
        id = data.get("id")
        if not id:
            return BaseResponse.badRequest("Dữ liệu không hợp lệ")

        account = AccountsRepo.getByID(id)
        if not account:
            return BaseResponse.notFound("Không tìm thấy tài khoản")

        email = data.get("email")
        if email and AccountsRepo.getByEmail(email) and account.email != email:
            return BaseResponse.conflict("Email đã được sử dụng")

        account.email = email or account.email
        account.password = data.get("password", account.password)
        account.isActive = data.get("isActive", account.isActive)
        updated = AccountsRepo.update(account)
        return BaseResponse.success(
            "Cập nhật tài khoản thành công", AccountSerializer(updated).data
        )

    @staticmethod
    def doDelete(data: dict):
        id = data.get("id")
        if not id:
            return BaseResponse.badRequest("Dữ liệu không hợp lệ")
        deleted = AccountsRepo.delete(id)
        if deleted:
            return BaseResponse.success("Xoá tài khoản thành công")
        return BaseResponse.notFound("Không tìm thấy tài khoản")
