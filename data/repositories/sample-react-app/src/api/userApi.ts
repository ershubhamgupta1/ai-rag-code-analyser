import axios from "axios";

export const getUsers = () => {
  return axios.get("/api/users");
};

export const createUser = (
  data: any
) => {
  return axios.post(
    "/api/users",
    data
  );
};