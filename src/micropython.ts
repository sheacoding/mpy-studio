import { SerialPort } from 'serialport';
import fs from 'fs';
import path from 'path';
import { ReadlineParser } from '@serialport/parser-readline';

function sleep(millis: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, millis));
}

function fixLineBreak(str: string): string {
  return str.replace(/\r\n/g, '\n');
}

function extract(out: string): string {
  return out.slice(2, -3);
}

function extractBytes(out: string, cut_before = 2, cut_after = 3): number[] {
  let bytes = out.slice(cut_before, -cut_after);
  return bytes.split(',').map(Number);
}

class MicroPythonBoard {
  port: any = null;
  serial: any = null;
  parser: any = null;
  reject_run: any = null;

  list_ports() {
    return SerialPort.list();
  }

  async open(port: string) {
    if (port) {
      this.port = port;
    } else {
      return Promise.reject(new Error(`No device specified`));
    }
    if (this.serial && this.serial.isOpen) {
      await this.serial.close();
      this.serial = null;
    }
    this.serial = new SerialPort({
      path: this.port,
      baudRate: 115200,
      lock: false,
      autoOpen: false
    });
    this.serial.pause();
    this.parser = this.serial.pipe(new ReadlineParser({ delimiter: '\n' }));
    return new Promise((resolve, reject) => {
      this.serial.open(async (err: any) => {
        if (err) {
          reject(err);
        } else {
          resolve(null);
        }
      });
    });
  }

  close() {
    if (this.serial && this.serial.isOpen) {
      return this.serial.close();
    } else {
      return Promise.resolve();
    }
  }

  read_until(ending: string, data_consumer?: (data: string) => void) {
    return new Promise((resolve, reject) => {
      let buff = '';
      const fn = async () => {
        const o = await this.serial.read();
        if (o) {
          buff += o.toString();
          if (data_consumer) {
            data_consumer(o.toString());
          }
        }
        if (buff.indexOf(ending) !== -1) {
          this.serial.removeListener('readable', fn);
          resolve(buff);
        }
      };
      this.serial.on('readable', fn);
    });
  }

  async write_and_read_until(cmd: string, expect?: string, data_consumer?: (data: string) => void) {
    this.serial.pause();
    const chunkSize = 128;
    for (let i = 0; i < cmd.length; i += chunkSize) {
      const s = cmd.slice(i, i + chunkSize);
      await this.serial.write(Buffer.from(s));
      await sleep(10);
    }
    let o;
    if (expect) {
      o = await this.read_until(expect, data_consumer);
    }
    await this.serial.flush();
    await sleep(10);
    this.serial.resume();
    return o;
  }

  async get_prompt() {
    await sleep(150);
    await this.stop();
    await sleep(150);
    const out = await this.write_and_read_until(`\r\x03\x02`, '\r\n>>>');
    return Promise.resolve(out);
  }

  async enter_raw_repl() {
    const out = await this.write_and_read_until(`\x01`, `raw REPL; CTRL-B to exit`);
    return Promise.resolve(out);
  }

  async exit_raw_repl() {
    const out = await this.write_and_read_until(`\x02`, '\r\n>>>');
    return Promise.resolve(out);
  }

  async exec_raw(cmd: string, data_consumer?: (data: string) => void) {
    await this.write_and_read_until(cmd);
    const out = await this.write_and_read_until('\x04', '\x04>', data_consumer) as string;
    return Promise.resolve(out);
  }

  async execfile(filePath: string, data_consumer?: (data: string) => void) {
    data_consumer = data_consumer || function () { };
    if (filePath) {
      const content = fs.readFileSync(path.resolve(filePath));
      await this.enter_raw_repl();
      const output = await this.exec_raw(content.toString(), data_consumer);
      await this.exit_raw_repl();
      return Promise.resolve(output);
    }
    return Promise.reject();
  }

  async run(code: string, data_consumer?: (data: string) => void) {
    data_consumer = data_consumer || function () { };
    return new Promise(async (resolve, reject) => {
      if (this.reject_run) {
        this.reject_run(new Error('re-run'));
        this.reject_run = null;
      }
      this.reject_run = reject;
      try {
        await this.enter_raw_repl();
        const output = await this.exec_raw(code || '#', data_consumer);
        await this.exit_raw_repl();
        return resolve(output);
      } catch (e) {
        reject(e);
        this.reject_run = null;
      }
    });
  }

  async eval(k: string) {
    await this.serial.write(Buffer.from(k));
    return Promise.resolve();
  }

  async stop() {
    if (this.reject_run) {
      this.reject_run(new Error('pre stop'));
      this.reject_run = null;
    }
    await this.serial.write(Buffer.from(`\x03`));
    return Promise.resolve();
  }

  async reset() {
    if (this.reject_run) {
      this.reject_run(new Error('pre reset'));
      this.reject_run = null;
    }
    await this.serial.write(Buffer.from(`\x03`));
    await this.serial.write(Buffer.from(`\x04`));
    return Promise.resolve();
  }

  async fs_exists(filePath: string) {
    filePath = filePath || '';
    let command = `try:\n`;
    command += `  f = open(\"${filePath}\", \"r\")\n`;
    command += `  print(1)\n`;
    command += `except OSError:\n`;
    command += `  print(0)\n`;
    command += `del f\n`;
    await this.enter_raw_repl();
    let output = await this.exec_raw(command) as string;
    await this.exit_raw_repl();
    const exists = output[2] == '1';
    return Promise.resolve(exists);
  }

  async fs_ls(folderPath: string) {
    folderPath = folderPath || '';
    let command = `import uos\n`;
    command += `try:\n`;
    command += `  l=[]\n`;
    command += `  for f in uos.ilistdir(\"${folderPath}\"):\n`;
    command += `    l.append({'name': f[0], 'type': 'folder' if f[1]==0x4000 else 'file'})\n`;
    command += `  print(l)\n`;
    command += `except OSError:\n`;
    command += `  print([])\n`;
    await this.enter_raw_repl();
    let output = await this.exec_raw(command) as string;
    await this.exit_raw_repl();
    output = extract(output);
    output = output.replace(/'/g, '"');
    const files = JSON.parse(output);
    return Promise.resolve(files);
  }

  async fs_cat_binary(filePath: string) {
    if (filePath) {
      await this.enter_raw_repl();
      const chunkSize = 256;
      let command = `with open('${filePath}','rb') as f:\n`;
      command += `  while 1:\n`;
      command += `    b=f.read(${chunkSize})\n`;
      command += `    if not b:break\n`;
      command += `    print(",".join(str(e) for e in b),end=',')\n`;
      command += `del f\n`;
      command += `del b\n`;
      let output = await this.exec_raw(command) as string;
      await this.exit_raw_repl();
      let files = extractBytes(output, 2, 4);
      return Promise.resolve(files);
    }
    return Promise.reject(new Error(`Path to file was not specified`));
  }

  async fs_cat(filePath: string) {
    if (filePath) {
      await this.enter_raw_repl();
      let output = await this.exec_raw(
        `with open('${filePath}','r') as f:\n while 1:\n  b=f.read(256)\n  if not b:break\n  print(b,end='')\ndel f\ndel b\n`
      ) as string;
      await this.exit_raw_repl();
      output = extract(output);
      return Promise.resolve(fixLineBreak(output));
    }
    return Promise.reject(new Error(`Path to file was not specified`));
  }

  async fs_put(src: string, dest: string, data_consumer?: (data: string) => void) {
    data_consumer = data_consumer || function () { };
    if (src && dest) {
      const fileContent = fs.readFileSync(path.resolve(src), 'binary')
      const contentBuffer =  Buffer.from(fileContent, 'binary')
      let out = '';
      out += await this.enter_raw_repl();
      out += await this.exec_raw(`f=open('${dest}','wb')\nw=f.write`);
      const chunkSize = 256;
      for (let i = 0; i < contentBuffer.length; i += chunkSize) {
        let slice = Uint8Array.from(contentBuffer.subarray(i, i + chunkSize));
        let line = `w(bytes([${slice}]))`
        out += await this.exec_raw(line) as string;
        data_consumer(Math.floor((i / contentBuffer.length) * 100).toString() + '%');
      }
      out += await this.exec_raw(`f.close()\ndel f\ndel w\n`);
      out += await this.exit_raw_repl();
      return Promise.resolve(out);
    }
    return Promise.reject(new Error(`Must specify source and destination paths`));
  }

  async fs_save(content: string, dest: string, data_consumer?: (data: string) => void) {
    data_consumer = data_consumer || function () { };
    if (typeof dest === 'string' && dest.length > 0) {
      const contentBuffer = Buffer.from(content || '', 'utf-8');
      let out = '';
      out += await this.enter_raw_repl();
      out += await this.exec_raw(`f=open('${dest}','wb')\nw=f.write`);
      const chunkSize = 48;
      for (let i = 0; i < contentBuffer.length; i += chunkSize) {
        let slice = Uint8Array.from(contentBuffer.subarray(i, i + chunkSize));
        let line = `w(bytes([${slice}]))`;
        out += await this.exec_raw(line) as string;
        data_consumer(Math.floor((i / contentBuffer.length) * 100).toString() + '%');
      }
      out += await this.exec_raw(`f.close()\ndel f\ndel w\n`);
      out += await this.exit_raw_repl();
      return Promise.resolve(out);
    } else {
      return Promise.reject(new Error(`Must specify destination path`));
    }
  }

  async fs_mkdir(filePath: string) {
    if (filePath) {
      await this.enter_raw_repl();
      const output = await this.exec_raw(
        `import uos\nuos.mkdir('${filePath}')`
      ) as string;
      await this.exit_raw_repl();
      return Promise.resolve(output);
    }
    return Promise.reject();
  }

  async fs_rmdir(filePath: string) {
    if (filePath) {
      let command = `import uos\n`;
      command += `try:\n`;
      command += `  uos.rmdir(\"${filePath}\")\n`;
      command += `except OSError:\n`;
      command += `  print(0)\n`;
      await this.enter_raw_repl();
      const output = await this.exec_raw(command) as string;
      await this.exit_raw_repl();
      return Promise.resolve(output);
    }
    return Promise.reject();
  }

  async fs_rm(filePath: string) {
    if (filePath) {
      let command = `import uos\n`;
      command += `try:\n`;
      command += `  uos.remove(\"${filePath}\")\n`;
      command += `except OSError:\n`;
      command += `  print(0)\n`;
      await this.enter_raw_repl();
      const output = await this.exec_raw(command) as string;
      return this.exit_raw_repl();
    }
    return Promise.reject();
  }

  async fs_rename(oldFilePath: string, newFilePath: string) {
    if (oldFilePath && newFilePath) {
      await this.enter_raw_repl();
      const output = await this.exec_raw(
        `import uos\nuos.rename('${oldFilePath}', '${newFilePath}')`
      ) as string;
      return this.exit_raw_repl();
    }
    return Promise.reject();
  }

  async get_root(): Promise<string> {
    // 执行 helpers.py 的 get_root 并返回结果
    await this.enter_raw_repl();
    const output = await this.exec_raw('get_root()') as string;
    await this.exit_raw_repl();
    // 提取 OK ... \x04 之间的内容
    const str = typeof output === 'string' ? output : (output !== undefined && output !== null ? String(output) : '');
    return str.substring(str.indexOf('OK') + 2, str.indexOf('\x04'));
  }
}

export default MicroPythonBoard; 