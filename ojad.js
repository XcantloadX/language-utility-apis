const axios = require('axios');
const { parse } = require('node-html-parser');

async function verb_conjugations(word) {
	const url = 'http://www.gavo.t.u-tokyo.ac.jp/ojad/search/index/display:print/sortprefix:accent/narabi1:kata_asc/narabi2:accent_asc/narabi3:mola_asc/yure:visible/curve:invisible/details:invisible/limit:500/word:' + word;
	const { status, data } = await axios.get(url, { headers: {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'} });
	const root = parse(data);
	const word_row = root.querySelector('#word_table tbody tr');
	// console.log(word_row.toString());
	return {
		query: word,
		conjugations: {
			jisho: word_row.querySelector('.katsuyo.katsuyo_jisho_js').text.trim(),
			masu: word_row.querySelector('.katsuyo.katsuyo_masu_js').text.trim(),
			te: word_row.querySelector('.katsuyo.katsuyo_te_js').text.trim(),
			ta: word_row.querySelector('.katsuyo.katsuyo_ta_js').text.trim(),
			nai: word_row.querySelector('.katsuyo.katsuyo_nai_js').text.trim(),
			nakatta: word_row.querySelector('.katsuyo.katsuyo_nakatta_js').text.trim(),
			ba: word_row.querySelector('.katsuyo.katsuyo_ba_js').text.trim(),
			shieki: word_row.querySelector('.katsuyo.katsuyo_shieki_js').text.trim(),
			ukemi: word_row.querySelector('.katsuyo.katsuyo_ukemi_js').text.trim(),
			meirei: word_row.querySelector('.katsuyo.katsuyo_meirei_js').text.trim(),
			kano: word_row.querySelector('.katsuyo.katsuyo_kano_js').text.trim(),
			ishi: word_row.querySelector('.katsuyo.katsuyo_ishi_js').text.trim(),
		}
	};
}

module.exports = {
	verb_conjugations
};