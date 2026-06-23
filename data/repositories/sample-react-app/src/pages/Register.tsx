import { useState } from "react";

import { registerApi }
from "../api/authApi";

export default function Register() {

  const [name, setName] =
    useState("");

  const [email, setEmail] =
    useState("");

  const register =
    async () => {

      await registerApi({
        name,
        email
      });
    };

  return (
    <button
      onClick={register}
    >
      Register
    </button>
  );
}