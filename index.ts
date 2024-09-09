import { WechatyBuilder, Contact, Room, Message, ScanStatus, log } from 'wechaty';
import { ContactImpl } from 'wechaty/impls';
import qrcodeTerminal from 'qrcode-terminal';
import { FileBox } from 'file-box';
import * as fs from 'fs';
import * as path from 'path';

const wechaty = WechatyBuilder.build();

function displayStartupBanner() {
  const banner = `
  ____    __  __    _    _     _     ____   ___ _____
 / ___|  |  \\/  |  / \\  | |   | |   | __ ) / _ \\_   _|
 \\___ \\  | |\\/| | / _ \\ | |   | |   |  _ \\| | | || |
  ___) | | |  | |/ ___ \\| |___| |___| |_) | |_| || |
 |____/  |_|  |_/_/   \\_\\_____|_____|____/ \\___/ |_|

`;

  console.log('\x1b[36m%s\x1b[0m', banner);
  console.log('\x1b[33m%s\x1b[0m', '🚀 WX Job Bot is starting up!');
}

wechaty
  .on('scan', (qrcode: string, status) => {
    if (status === ScanStatus.Waiting || status === ScanStatus.Timeout) {
      const qrcodeImageUrl = ['https://wechaty.js.org/qrcode/', encodeURIComponent(qrcode)].join('');
      console.info('StarterBot', 'onScan: %s(%s) - %s', ScanStatus[status], status, qrcodeImageUrl);

      qrcodeTerminal.generate(qrcode, { small: true }); // 在控制台显示二维码
    } else {
      console.info('StarterBot', 'onScan: %s(%s)', ScanStatus[status], status);
    }
  })
  .on('login', async (user: ContactImpl) => {
    console.log('\x1b[36m%s\x1b[0m', `🎉 User ${user} logged in successfully!`);
  })
  .on('message', async (message: Message) => {
    console.log(`Received message: ${message.text()}`);
  });

displayStartupBanner();
wechaty.start();

async function onLogin(user: Contact) {
  console.log(`用户 ${user} 登录成功`);
  
  // 查找名为"测试群"的群聊
  const room = await wechaty.Room.find({ topic: '测试群' });
  
  if (room) {
    console.log('找到了"测试群"');
    const filePath = path.join(__dirname, 'jobs', 'filtered_recent_jobs.txt');
    
    // 监视文件变化
    fs.watch(filePath, async (eventType, filename) => {
      if (eventType === 'change') {
        try {
          const fileContent = fs.readFileSync(filePath, 'utf-8');
          await room.say('新的工作机会更新：');
          await room.say(fileContent);
          console.log('已发送 filtered_recent_jobs 文件内容到测试群');
        } catch (error) {
          console.error('读取或发送文件内容失败:', error);
        }
      }
    });
    
    console.log(`正在监视文件: ${filePath}`);
  } else {
    console.log('未找到"测试群"');
  }
}

wechaty.on('login', onLogin);