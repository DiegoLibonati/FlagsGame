import { useState } from "react";
import { FlagsContext } from "./FlagsContext";
import { useFetch } from "../hooks/useFetch";

export const FlagsProvider = ({ children }) => {
  const [navbar, setNavbar] = useState(false);
  const [btnStart, setBtnStart] = useState(false);
  const [score, setScore] = useState(0);
  const [flagsUrl, setFlagsUrl] = useState([]);
  const [modeUrl, setModeUrl] = useState([]);
  const [topUrl, setTopUrl] = useState([]);

  const {
    arrayData,
    isLoading,
    arrayMode,
    isLoadingMode,
    arrayTop,
    isLoadingTop,
  } = useFetch(flagsUrl, modeUrl, topUrl);

  const manageNavbar = () => {
    setNavbar(!navbar);
  };

  return (
    <FlagsContext.Provider
      value={{
        navbar,
        manageNavbar,
        arrayData,
        isLoading,
        setFlagsUrl,
        arrayMode,
        isLoadingMode,
        setModeUrl,
        btnStart,
        setBtnStart,
        score,
        setScore,
        arrayTop,
        isLoadingTop,
        setTopUrl,
      }}
    >
      {children}
    </FlagsContext.Provider>
  );
};
