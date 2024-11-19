import { parseAlertType } from "./parseAlertType";

test("It must return 'unknown' if an empty string is entered for parsing.", () => {
  const alertType = "";

  const alertTypeParsed = parseAlertType(alertType);

  expect(alertTypeParsed).toBe("unknown");
});

test("It must return 'error' if an 'alert-auth-error' string is entered for parsing.", () => {
  const alertType = "alert-auth-error";

  const alertTypeParsed = parseAlertType(alertType);

  expect(alertTypeParsed).toBe("error");
});

test("It should return 'success' if an 'alert-auth-success' string is entered for parsing.", () => {
  const alertType = "alert-auth-success";

  const alertTypeParsed = parseAlertType(alertType);

  expect(alertTypeParsed).toBe("success");
});
