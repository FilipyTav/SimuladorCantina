from typing import Literal, TypeAlias

TypeUser = Literal["aluno", "servidor", "professor"]
TypeCourse = Literal["IA", "ESG"]
UserInfo: TypeAlias = tuple[str, TypeUser, TypeCourse]
