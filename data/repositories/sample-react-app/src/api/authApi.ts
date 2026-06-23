import axios from "axios";

export const loginApi = (email: string, password: string) => {
  return axios.post("/api/login", {
    email,
    password,
  });
};

export const registerApi = (data: any) => {
  return axios.post("/api/register", data);
};