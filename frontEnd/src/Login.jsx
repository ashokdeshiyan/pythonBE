import { apiRequest } from "./api";

const inputClasses =
  "w-full p-2 text-base border border-gray-300 rounded mb-2";

export default function Login({ onShow }) {
  const handleSubmit = async (e) => {
    e.preventDefault();
    const form = e.target;
    const body = {
      email: form.email.value,
      password: form.password.value,
    };
    const result = await apiRequest("login", body);
    onShow(result.ok, result.message);
    if (result.ok) form.reset();
  };

  return (
    <form id="login" onSubmit={handleSubmit} className="grid gap-2">
      <h2 className="text-xl font-bold mb-2">Login</h2>
      <input
        name="email"
        type="email"
        placeholder="Email"
        required
        className={inputClasses}
      />
      <input
        name="password"
        type="password"
        placeholder="Password"
        required
        className={inputClasses}
      />
      <button
        type="submit"
        className="p-2 text-base bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Login
      </button>
    </form>
  );
}
