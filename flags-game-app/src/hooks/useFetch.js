import { useEffect, useState } from "react";

export const useFetch = (urlFlags, urlMode, urlTop) => {
  const [array, setArray] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const [arrayMode, setArrayMode] = useState([]);
  const [isLoadingMode, setIsLoadingMode] = useState(false);

  const [arrayTop, setArrayTop] = useState([]);
  const [isLoadingTop, setIsLoadingTop] = useState(false);

  const getAllFlags = async () => {
    try {
      setIsLoading(true);

      const request = await fetch(urlFlags);
      const data = await request.json();

      setArray(data);
      setIsLoading(false);
    } catch (e) {}
  };

  const getMode = async () => {
    try {
      setIsLoadingMode(true);

      const request = await fetch(urlMode);
      const data = await request.json();
      setArrayMode(data);
      setIsLoadingMode(false);
    } catch (e) {}
  };

  const getTop = async () => {
    try {
      setIsLoadingTop(true);

      const request = await fetch(urlTop);
      const data = await request.json();
      setArrayTop(data);
      setIsLoadingTop(false);
    } catch (e) {}
  };

  useEffect(() => {
    getAllFlags();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [urlFlags]);

  useEffect(() => {
    getMode();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [urlMode]);

  useEffect(() => {
    getTop();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [urlTop]);

  return {
    arrayData: array,
    isLoading: isLoading,
    arrayMode: arrayMode,
    isLoadingMode: isLoadingMode,
    arrayTop: arrayTop,
    isLoadingTop: isLoadingTop,
  };
};
