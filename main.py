import logging
import matplotlib.pyplot as plt
import argparse
import stocks


def setup_logger():
    logging.basicConfig(
        filename="main.log",
        format="[%(levelname)s] %(asctime)s : %(message)s",
        encoding="utf-8",
        level=logging.INFO,
    )


def main(args):
    db = stocks.StocksDB("data")
    table = stocks.Table(db=db)
    plot = stocks.Plot(db=db,start=args.start,end=args.end)

    if args.plot:
        
        if (args.plot[0] == "all"):    
            plot.plot_all()

        elif(args.plot[0] == "aapl"):
            plot.plot(args.plot)

    elif args.candle:
        plot.candlestick(args.candle)

    
    if args.table:
        table.print(args.table,args.limit)
        


if __name__ == "__main__":
    setup_logger()

    # -------------------------------------
    # Command line input parser
    # -------------------------------------
    arg_parser = argparse.ArgumentParser()

    # table/limit arguments
    arg_parser.add_argument(
    "--table",type=str, help="Key through which the desired table needs to be sorted"
    )

    arg_parser.add_argument(
    "--limit",type=int, help="limit the number of stocks to the given number of entries"
    )
    
    # add start/end aguments
    arg_parser.add_argument(
    "--start",type=str, help="Start date provided in YYYY-MM-DD format"
    )

    arg_parser.add_argument(
    "--end",type=str, help="End date provided in YYYY-MM-DD format"
    )
    
    # add plot/candle arguments

    arg_parser.add_argument("--plot", nargs="*", type=str, help="Plot the data using a time series plot")
    arg_parser.add_argument("--candle", type=str, help="Plot the data using a candlestick plot")
    
    args = arg_parser.parse_args()

    # -------------------------------------
    logging.info(f"Started running main.py: args: {args}")
    # -------------------------------------

    main(args)
