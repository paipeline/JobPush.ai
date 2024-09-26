import { WechatyBuilder, Contact, Room, Message, ScanStatus, log } from 'wechaty'; // whatsapp facebook - frontend
import { ContactImpl } from 'wechaty/impls';
import qrcodeTerminal from 'qrcode-terminal';
import { FileBox } from 'file-box';
import * as fs from 'fs';
import * as path from 'path';

const wechaty = WechatyBuilder.build();

function displayStartupBanner() {
  const banner = `
     _    ___ ___      _     ____        _   
    / \\  |_ _|_ _|    | |   | __ )  ___ | |_ 
   / _ \\  | | | |  _  | |   |  _ \\ / _ \\| __|
  / ___ \\ | | | | | |_| |   | |_) | (_) | |_ 
 /_/   \\_\\___|___| \\___/    |____/ \\___/ \\__|
                                             
  Your AI-powered Job Search Assistant
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
    console.log('\x1b[36m%s\x1b[0m', `🎉 用户 ${user} 登录成功！`);
  })
  .on('message', async (message: Message) => {
    console.log(`收到消息: ${message.text()}`);
  });

displayStartupBanner();
wechaty.start();

async function sendJobUpdate(room: Room, filePath: string, category: string) {
  try {
    const fileContent = fs.readFileSync(filePath, 'utf-8');
    // 将文件内容分块发送，每块不超过4000字符
    const chunkSize = 4000;
    for (let i = 0; i < fileContent.length; i += chunkSize) {
      const chunk = fileContent.slice(i, i + chunkSize);
      await room.say(chunk);
      // 添加短暂延迟，避免消息发送过快
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
    
    console.log(`已发送 ${category} 工作信息到测试群`);
  } catch (error) {
    console.error(`读取或发送 ${category} 文件内容失败:`, error);
  }
}

async function onLogin(user: Contact) {
  console.log(`用户 ${user} 登录成功`);
  
  // 查找名为"测试群"的群聊
  const room = await wechaty.Room.find({ topic: '测试群' });
  
  if (room) {
    console.log('找到了"测试群"');
    const jobsDir = path.join(__dirname, 'src/jobs');
    
    // 获取当前日期
    const currentDate = new Date();
    const formattedDate = `${currentDate.getFullYear()}-${String(currentDate.getMonth() + 1).padStart(2, '0')}-${String(currentDate.getDate()).padStart(2, '0')}`;

    // 查找并发送当天的工作信息
    fs.readdir(jobsDir, async (err, files) => {
      if (err) {
        console.error('读取目录失败:', err);
        return;
      }

      for (const file of files) {
        if (file.startsWith(`formatted_jobs_`) && file.endsWith(`${formattedDate}.txt`)) {
          const filePath = path.join(jobsDir, file);
          const category = file.split('_')[2]; // 提取类别名称
          await sendJobUpdate(room, filePath, category);
        }
      }
    });
    
    console.log(`正在处理 ${formattedDate} 的工作信息`);
  } else {
    console.log('未找到"测试群"');
  }
}

wechaty.on('login', onLogin);