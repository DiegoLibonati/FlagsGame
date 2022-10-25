import { useContext } from "react";
import "./ModePage.css";
import { FlagsContext } from "../context/FlagsContext";
import { useEffect } from "react";
import { Loader } from "../components/Loader";
import { useLocation, useParams, Link } from "react-router-dom";
import { useCountdown } from "../hooks/useCountdown";
import { Flag } from "../components/Flag";
import { useLogic } from "../hooks/useLogic";
import { useForm } from "../hooks/useForm";
import { BsChevronLeft } from "react-icons/bs";
import { useRef } from "react";

export const ModePage = () => {
  const {
    arrayData,
    isLoading,
    setFlagsUrl,
    btnStart,
    setBtnStart,
    arrayMode,
    score,
    setScore,
  } = useContext(FlagsContext);

  const { timeleft } = arrayMode;
  const { mode } = useParams();
  const input = useRef();
  const { timer, onClickReset } = useCountdown(timeleft, mode);

  const { formState, onInputChange, onResetForm } = useForm({
    name: "",
  });

  const { currentItem, onSubmit, setFinishGame } = useLogic(
    arrayData,
    formState.name,
    onResetForm,
    timer,
    setScore,
    score,
    mode,
    input
  );

  const location = useLocation();

  useEffect(() => {
    setFlagsUrl(`http://127.0.0.1:5000/flags/${mode}`);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    setBtnStart(false);
    setFinishGame(false);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [location]);

  const startGame = () => {
    setBtnStart(true);
    onClickReset();
  };

  if (isLoading) {
    return (
      <main>
        <Loader></Loader>
      </main>
    );
  } else {
    if (btnStart) {
      return (
        <>
          <main>
            <section className="guess_container">
              <article className="guess_container_header">
                <h1>GUESS THE FLAG</h1>
                <Flag key={currentItem._id.$oid} {...currentItem}></Flag>
              </article>

              <form
                className="guess_container_form"
                onSubmit={(e) => onSubmit(e)}
              >
                <input
                  ref={input}
                  type="text"
                  value={formState.name}
                  onChange={(e) => onInputChange(e)}
                  name="name"
                ></input>
                <button>SUBMIT</button>
              </form>

              <article className="guess_container_score">
                <h3>Score: {score} PTS</h3>

                <h3>Time left: {timer}</h3>
              </article>
            </section>
          </main>
        </>
      );
    } else {
      return (
        <main>
          <Link to={`/menu/${mode}`}>
            <BsChevronLeft id="go-back"></BsChevronLeft>
          </Link>
          <section className="section_btn_start">
            <button
              type="text"
              onClick={() => startGame()}
              className="btn-start-game"
            >
              START GAME
            </button>
          </section>
        </main>
      );
    }
  }
};
