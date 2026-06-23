import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav>
      <ul>
        <li>
          <Link to="/">
            Dashboard
          </Link>
        </li>

        <li>
          <Link to="/users">
            Users
          </Link>
        </li>

        <li>
          <Link to="/login">
            Login
          </Link>
        </li>

        <li>
          <Link to="/register">
            Register
          </Link>
        </li>
      </ul>
    </nav>
  );
}