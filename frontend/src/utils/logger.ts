type LogLevel = 'INFO' | 'WARN' | 'ERROR';

class Logger {
  private static formatMessage(
    level: LogLevel,
    message: string,
    data?: any,
  ): string {
    const timestamp = new Date().toISOString();
    const formattedData = data
      ? `\nData: ${JSON.stringify(data, null, 2)}`
      : '';
    return `[${timestamp}] [${level}] ${message}${formattedData}`;
  }

  static info(message: string, data?: any) {
    console.log(this.formatMessage('INFO', message, data));
  }

  static warn(message: string, data?: any) {
    console.warn(this.formatMessage('WARN', message, data));
  }

  static error(message: string, data?: any) {
    console.error(this.formatMessage('ERROR', message, data));
  }
}

export default Logger;
