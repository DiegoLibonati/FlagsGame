import {
  AlertContext,
  Flag,
  Mode,
  UserWithOutPassword,
} from "../entities/entities";

export const FLAGS_DATA_STATIC_TEST: Flag[] = [
  {
    _id: "6728cc43d19b644f5bc6e495",
    image:
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQilbazSxXoEzGPXF0J5Oy3FzGUAgxuMu7upg&s",
    name: "Colombia",
  },
  {
    _id: "672680152e10fe5f0af5d707",
    image:
      "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Flag_of_Brazil.svg/1200px-Flag_of_Brazil.svg.png",
    name: "Brasil",
  },
  {
    _id: "672681bf0291c4ae90b6798e",
    image:
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS-bu9g_Be9LrSEFgXHGT0jX11SCVgzZNaOfA&s",
    name: "Estados Unidos",
  },
  {
    _id: "67267fd72e10fe5f0af5d706",
    image:
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVnagHgbpRUO82-sIOEi3TX1N3wUGSlRWKZQ&s",
    name: "Argentina",
  },
  {
    _id: "6726819e0291c4ae90b6798c",
    image:
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQt5fAr3G2SRs1TaR3jSiGhYPOdxu4mj8sBtg&s",
    name: "Peru",
  },
];

export const FLAG_DATA_STATIC_TEST: Flag = FLAGS_DATA_STATIC_TEST[0];

export const MODES_DATA_STATIC_TEST: Mode[] = [
  {
    _id: "672687090bcd13f7c9a88ac3",
    description: "You must guess the most available flags in 90 seconds.",
    multiplier: 10,
    name: "Normal",
    timeleft: 90,
  },
  {
    _id: "6726874dde5266d8ba53ae77",
    description: "You must guess the most available flags in 60 seconds.",
    multiplier: 25,
    name: "Hard",
    timeleft: 60,
  },
  {
    _id: "67268757de5266d8ba53ae78",
    description: "You must guess the most available flags in 25 seconds.",
    multiplier: 100,
    name: "Hardcore",
    timeleft: 25,
  },
];

export const MODE_DATA_STATIC_TEST: Mode = MODES_DATA_STATIC_TEST[0];

export const USERS_TOP_STATIC_TEST: UserWithOutPassword[] = [
  {
    _id: "672a713141aec0b5e6b0a1a2",
    score: 6925,
    username: "TITO",
  },
  {
    _id: "672b76e474e247da51a8bd3a",
    score: 6925,
    username: "pipo",
  },
  {
    _id: "672a2af08d61f5bc12a53a22",
    score: 4240,
    username: "carlos",
  },
  {
    _id: "672a2b518d61f5bc12a53a23",
    score: 4240,
    username: "that",
  },
  {
    _id: "672a2bec8d61f5bc12a53a24",
    score: 4240,
    username: "asd2",
  },
  {
    _id: "672a2bf28d61f5bc12a53a25",
    score: 4240,
    username: "thah",
  },
  {
    _id: "672a2c138d61f5bc12a53a26",
    score: 4240,
    username: "1234",
  },
  {
    _id: "672d7d63fc37bd87b814120b",
    score: 4160,
    username: "kakita",
  },
  {
    _id: "672a54044fb7fbdad3c57bcd",
    score: 2200,
    username: "sklere",
  },
  {
    _id: "672a6a7018808b8d2488b76b",
    score: 1233,
    username: "pepetest",
  },
  {
    _id: "672a717a41aec0b5e6b0a1a3",
    score: 1000,
    username: "pepetest3",
  },
  {
    _id: "6726bfcb1aca726cd98bd51a",
    score: 120,
    username: "pepe",
  },
];

export const FIRST_USER_TOP_STATIC: UserWithOutPassword =
  USERS_TOP_STATIC_TEST[0];

export const ALERT_PROVIDER_STATIC: AlertContext = {
  alert: {
    message: "",
    type: "",
  },
  handleClearAlert: jest.fn(),
  handleSetAlert: jest.fn(),
};
