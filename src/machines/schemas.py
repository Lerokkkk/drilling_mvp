from datetime import datetime

from pydantic import BaseModel


class BaseMachine(BaseModel):
    machine_name: str
    startup_status: bool
    status: bool
    write_way: str | None = None
    start_time: datetime | None = None
    loadfile_path: str | None = None
    hot_reload: str
    ready_ip: list[str] | None = None
    check_time: int
    input_command: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "machine_name": "Bentec",
                    "startup_status": True,
                    "status": True,
                    "write_way": "local",
                    "start_time": datetime.now(),
                    "loadfile_path": r"c//",
                    "hot_reload": "extra",
                    "ready_ip": ["127.0.0.1", "413.1.1.021"],
                    "check_time": 2,
                    "input_command": "start"
                }
            ]
        }
    }


class ShowMachine(BaseMachine):
    id: int

    class Config:
        from_attributes = True


class CreateMachine(BaseMachine):
    pass


class UpdateMachine(BaseModel):
    machine_name: str | None = None
    startup_status: bool | None = None
    status: bool | None = None
    write_way: str | None = None
    start_time: datetime | None = None
    loadfile_path: str | None = None
    hot_reload: str | None = None
    ready_ip: list[str] | None = None
    check_time: int | None = None
    input_command: str | None = None
