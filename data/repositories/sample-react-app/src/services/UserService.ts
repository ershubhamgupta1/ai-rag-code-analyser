import {
  getUsers,
  createUser
}
from "../api/userApi";

export class UserService {

  static async fetchUsers() {

    return getUsers();
  }

  static async addUser(
    data: any
  ) {

    return createUser(data);
  }
}