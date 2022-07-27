module.exports = {
  apps : [{
    // App 名稱
    name: '1432server',
    // script
    script: 'main.py',
    // 執行服務的入口
    cwd: '/home/thiits/1432/server',
    // 調用
    interpreter: "python3",
    // log 顯示時間
    time: true,          
    // log 的時間格式
    log_date_format: 'YYYY-MM-DD HH:mm Z',
    // 錯誤 log 的指定位置
    error_file: './log',
    // 正常輸出 log 的指定位置
    out_file: './log',
    // 同一個 app 有多程序 id, 如果設定為 true 的話， 同 app 的 log 檔案將不會根據不同的程序 id 分割，會全部合在一起
    combine_logs: true,
    // 同上
    merge_logs: true,
    // 預設為 true, 若設為 false, pm2 將會關閉自動重啟功能, 也就是說 app crash 之後將不會自動重啟
    autorestart: false,
    env: {
      ENV: 'development'
    },
    env_production : {
      ENV: 'production'
    }
  }]
};
