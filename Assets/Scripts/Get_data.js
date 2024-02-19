export async function get_data(url) {
  try {
    const req = await fetch(url);
    const data = await req.json();
    return data;
  } catch (e) {
    console.log(
      `Failed to call:${url}, will use placeholders if possible, error: ` +
        e.message
    );
    return 500;
  }
}
