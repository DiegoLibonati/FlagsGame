import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export const useRequest = (
  username,
  password,
  score,
  mode_name,
  url,
  resetForm
) => {
  const [alert, setAlert] = useState({
    type: "",
    message: "",
  });

  const navigate = useNavigate();

  const onSendRequest = async (e, method) => {
    e.preventDefault();

    const body = {
      username: username,
      password: password,
      score: score,
      mode_name: mode_name,
    };

    const result = await fetch(url, {
      method: method,
      body: JSON.stringify(body),
      headers: {
        "Content-Type": "application/json",
      },
    });

    const messageBody = await result.json();

    const { message } = messageBody;

    if (result.status === 200) {
      setAlert({ ...alert, type: "success", message: message });
    } else {
      setAlert({ ...alert, type: "error", message: message });
    }

    resetForm();
  };

  useEffect(() => {
    const timeout = setTimeout(() => {
      setAlert({ ...alert, type: "", message: "" });
    }, 2000);

    const redirect = setTimeout(() => {
      if (alert.type === "success") {
        navigate("/");
      }
    }, 1500);

    return () => {
      clearTimeout(timeout);
      clearTimeout(redirect);
    };
  }, [alert, navigate]);

  return {
    onSendRequest,
    alert,
  };
};
