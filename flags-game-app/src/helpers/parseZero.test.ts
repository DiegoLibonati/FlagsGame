import { parseZero } from "@src/helpers/parseZero";

describe("parseZero.ts", () => {
  describe("General Tests.", () => {
    test("It must return the number entered by parameters as a string but without adding the zero because it is greater than or equal to 10.", () => {
      const number = 12;

      const parsedString = parseZero(number);

      expect(parsedString).toBe(String(number));
    });

    test("It must return the number entered by parameters as a string but adding the zero because it is less than 10.", () => {
      const number = 9;

      const parsedString = parseZero(number);

      expect(parsedString).toBe(String(`0${number}`));
    });
  });
});
