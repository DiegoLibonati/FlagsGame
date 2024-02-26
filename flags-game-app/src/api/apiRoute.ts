const protocol = window.location.protocol + "//";
const hostname = window.location.hostname;
const port = window.location.port ? `:${window.location.port}` : "";

export const apiRouteFlags = protocol + hostname + port + "/v1/flags";
export const apiRouteModes = protocol + hostname + port + "/v1/modes";
export const apiRouteUsers = protocol + hostname + port + "/v1/users";
