import { useState } from "react";
import Register from "./Register";
import Login from "./Login";

export default function App() {
  const [msg, setMsg] = useState(null); // { ok: boolean, text: string }

  const show = (ok, text) => {
    setMsg({ ok, text });
    alert((ok ? "Success: " : "Error: ") + text);
  };

  return (
    <div className="max-w-md mx-auto p-4 mt-8 font-sans">
      <h1 className="text-2xl font-bold mb-6">Forum</h1>
      <div className="flex gap-8 flex-wrap">
        <Register onShow={show} />
        <Login onShow={show} />
      </div>
      {msg && (
        <div
          id="msg"
          role="status"
          className={`mt-4 p-2 whitespace-pre-wrap rounded ${
            msg.ok ? "bg-ok-bg" : "bg-err-bg"
          }`}
        >
          {msg.text}
        </div>
      )}
    </div>
  );
}
