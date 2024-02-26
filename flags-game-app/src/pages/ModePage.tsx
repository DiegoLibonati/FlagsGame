import { useContext } from "react";
import { FlagsContext } from "../context/FlagsContext";
import { useEffect } from "react";
import { Loader } from "../components/Loader";
import { useLocation, useParams, Link } from "react-router-dom";
import { useCountdown } from "../hooks/useCountdown";
import { Flag as FlagComponent } from "../components/Flag";
import { useLogic } from "../hooks/useLogic";
import { useForm } from "../hooks/useForm";
import { BsChevronLeft } from "react-icons/bs";
import { useRef } from "react";
import "./ModePage.css";
import { getRandomFlags } from "../api/getRandomFlags";

export const ModePage = (): JSX.Element => {
  const { mode } = useParams();
  const {
    flagsArr,
    flagsLoading,
    actualMode,
    score,
    btnStart,
    setBtnStart,
    setFlagsArr,
    setFlagsLoading,
    setScore,
  } = useContext(FlagsContext)!;
  const input = useRef<HTMLInputElement | null>(null);
  const { timer, onClickReset } = useCountdown(
    // TODO: WORK??
    actualMode!.timeleft,
    actualMode!.name
  );

  const { formState, onInputChange, onResetForm } = useForm<{ name: string }>({
    name: "",
  });

  const { currentItem, onSubmit, setFinishGame } = useLogic(
    flagsArr,
    formState.name,
    timer,
    score,
    mode!,
    input.current!,
    setScore,
    onResetForm
  );

  const location = useLocation();

  const handleFlags = async (): Promise<void> => {
    setFlagsLoading(true);

    const request = await getRandomFlags(mode!);

    const data = await request.json();

    setFlagsArr(data);

    setFlagsLoading(false);
  };

  useEffect(() => {
    handleFlags();
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

  if (flagsLoading) {
    return (
      <main>
        <Loader></Loader>
      </main>
    );
  } else {
    if (btnStart) {
      return (
        <main>
          <section className="guess_container">
            <article className="guess_container_header">
              <h1>GUESS THE FLAG</h1>
              <FlagComponent
                key={currentItem!._id!.$oid!}
                image={currentItem?.image!}
                name={currentItem?.name!}
              ></FlagComponent>
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
      );
    } else {
      return (
        <main>
          <Link to={`/menu/${mode}`}>
            <BsChevronLeft id="go-back"></BsChevronLeft>
          </Link>
          <section className="section_btn_start">
            <button
              type="button"
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
