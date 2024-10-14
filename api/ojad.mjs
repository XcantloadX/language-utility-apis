import { verb_conjugations } from '../ojad.js';

export default async function get(request, res) {
  const [, paramString ] = request.url.split('?');
  const params = new URLSearchParams(paramString);
  console.log(request.url);
  console.log(params.get('word'));
  const result = await verb_conjugations(params.get('word'));
  res.json(result);
}
export const maxDuration = 60;