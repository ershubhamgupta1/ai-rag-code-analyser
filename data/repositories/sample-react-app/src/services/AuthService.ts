import { loginApi } from "../api/authApi";

export class AuthService {

  static async login(
    email: string,
    password: string
  ) {

    const response =
      await loginApi(
        email,
        password
      );

    return response.data;
  }
}