import { useState } from "react";

import { AuthService }
from "../services/AuthService";

export default function Login() {

  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");

  const handleSubmit =
    async () => {

      await AuthService.login(
        email,
        password
      );
    };

  return (
    <button
      onClick={handleSubmit}
    >
      Login
    </button>
  );
}