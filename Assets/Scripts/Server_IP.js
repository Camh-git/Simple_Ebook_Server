export function Set_server_address(ip) {
  try {
    const expiry = new Date();
    expiry.setFullYear(expiry.getFullYear() + 1);
    if (ip.substring(0, 8) == "192.168." && ip.length < 16) {
      document.cookie = `IP=${ip}; expires=${expiry}`;
    } else {
      return "421";
    }
  } catch {
    //For when no IP is set
    return "400";
  }
}
try {
  //Try updating the cookie if already set, to prolong it's life
  Set_server_address(document.cookie.split("=")[1]);
} catch {
  Set_server_address();
}
