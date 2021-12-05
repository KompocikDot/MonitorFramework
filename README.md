# MonitorFramework

## Some important things
- **Go inside `kthread` module and change `isAlive` variable to `is_alive` - without it it will cause bugs due to syntax bug in this library**
- Inside settings.json you can set your webhook and timeout that framework look for changes in `links.csv` file
- `links.csv` is to send data into threads
- Don't try to input anything inside id column inside links.csv - it may cause strange behaviour
- Use `logging` to print inside every single thread

### Don't mind to add your things and help me make this repo better :)