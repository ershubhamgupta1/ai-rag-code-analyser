import {
  useState
} from "react";

import {
  UserService
}
from "../services/UserService";

export default function UserForm() {

  const [name, setName] =
    useState("");

  const saveUser =
    async () => {

      await UserService.addUser({
        name
      });
    };

  return (
    <button
      onClick={saveUser}
    >
      Save
    </button>
  );
}