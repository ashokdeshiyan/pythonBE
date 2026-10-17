import { apiRequest } from "./api";

const inputClasses =
  "w-full p-2 text-base border border-gray-300 rounded mb-2";

export default function Register({ onShow }) {
  const handleSubmit = async (e) => {
    e.preventDefault();
    const form = e.target;
    const body = {
      first_name: form.first_name.value,
      last_name: form.last_name.value,
      phone: form.phone.value,
      email: form.email.value,
      password: form.password.value,
    };
    const result = await apiRequest("registerusers", body);
    onShow(result.ok, result.message);
    if (result.ok) form.reset();
  };

  return (
    <form id="register" onSubmit={handleSubmit} className="grid gap-2">
      <h2 className="text-xl font-bold mb-2">Register</h2>
      <input
        name="first_name"
        placeholder="First name"
        required
        className={inputClasses}
      />
      <input
        name="last_name"
        placeholder="Last name"
        required
        className={inputClasses}
      />
      <input
        name="phone"
        type="tel"
        placeholder="Phone"
        pattern="[0-9+\-\s]{7,15}"
        required
        className={inputClasses}
      />
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
        minLength={6}
        required
        className={inputClasses}
      />
      <button
        type="submit"
        className="p-2 text-base bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Register
      </button>
    </form>
  );
}
