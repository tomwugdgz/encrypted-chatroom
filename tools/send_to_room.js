#!/usr/bin/env node
/**
 * 把消息发送到 cipher.room 聊天室。
 *
 * 依赖：playwright-core + 一个 Chromium 可执行文件
 *   npm i -g playwright-core
 *   设置 CHROME_PATH，例如 ~/.cache/ms-playwright/chromium-*/chrome-linux64/chrome
 *
 * 用法：
 *   node tools/send_to_room.js --url "<房间链接>" --nick "Tom" --file msgs.txt
 *   node tools/send_to_room.js --url "<房间链接>" --nick "Tom" --text "一条消息"
 *
 * --file 里每行算一条消息。空行跳过。
 */

const fs = require('fs');
const { chromium } = require('playwright-core');

function parseArgs(argv) {
  const out = { url: '', nick: '', file: '', text: '' };
  for (let i = 0; i < argv.length; i += 1) {
    if (argv[i] === '--url') out.url = argv[i + 1] || '';
    if (argv[i] === '--nick') out.nick = argv[i + 1] || '';
    if (argv[i] === '--file') out.file = argv[i + 1] || '';
    if (argv[i] === '--text') out.text = argv[i + 1] || '';
  }
  return out;
}

(async () => {
  const a = parseArgs(process.argv.slice(2));

  if (!a.url) {
    console.error('错误：缺少 --url');
    process.exit(2);
  }

  let messages = [];
  if (a.file) {
    messages = fs.readFileSync(a.file, 'utf8').split('\n')
      .map((s) => s.trim()).filter(Boolean);
  } else if (a.text) {
    messages = [a.text];
  }

  if (!messages.length) {
    console.error('错误：没有消息内容。用 --text 或 --file');
    process.exit(2);
  }

  const browser = await chromium.launch({
    executablePath: process.env.CHROME_PATH || undefined,
    headless: true,
    args: ['--no-sandbox', '--disable-dev-shm-usage'],
  });
  const page = await browser.newPage();
  await page.goto(a.url, { waitUntil: 'load' });
  await page.waitForTimeout(9000);

  for (const msg of messages) {
    if (a.nick) {
      await page.getByPlaceholder('Set a nickname (optional)').fill(a.nick);
    }
    await page.getByPlaceholder(/Type a message/).fill(msg);
    await page.getByRole('button', { name: 'Send' }).click();
    await page.waitForTimeout(1800);
    console.log('已发送 %d 字符', msg.length);
  }

  await page.waitForTimeout(2000);
  await browser.close();
  console.log('完成，共 %d 条', messages.length);
})().catch((e) => {
  console.error('FAIL:', e.message);
  process.exit(1);
});
