import { useEffect, useState } from "react";

import Navbar from "../components/Navbar";

import { UserService }
from "../services/UserService";

export default function Users() {

  const [users, setUsers] =
    useState([]);

  useEffect(() => {

    loadUsers();

  }, []);

  const loadUsers =
    async () => {

      const response =
        await UserService.fetchUsers();

      setUsers(
        response.data
      );
    };

  return (
    <>
      <Navbar />

      <h1>Users</h1>

      {users.map(
        (user: any) => (
          <div key={user.id}>
            {user.name}
          </div>
        )
      )}
    </>
  );
}