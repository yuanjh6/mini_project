import java.io.IOException;  
import jeasy.analysis.MMAnalyzer;  
import java.io.FileNotFoundException;  
import java.io.FileReader; 

public class JeAnalysis {
	 public static void main(String[] args) {  

	        String text = "全文检索是指计算机索引程序通过扫描文章中的每一个词，对每一个词建立一个索引，" +  
	                "指明该词在文章中出现的次数和位置，当用户查询时，检索程序就根据事先建立的索引进行查找，" +  
	                "并将查找的结果反馈给用户的检索方式。这个过程类似于通过字典中的检索字表查字的过程。";  
	        MMAnalyzer analyzer=new MMAnalyzer();  
	        try {  
	            FileReader rd=new FileReader("d://dic.txt");  
	            analyzer.addDictionary(rd);  
	        } catch (FileNotFoundException e1) {  
	            // TODO Auto-generated catch block  
	            e1.printStackTrace();  
	        }  
	      
	        try {  
	            System.out.println(analyzer.segment(text, " | "));  
	        } catch (Exception e) {  
	            // TODO: handle exception  
	            e.printStackTrace();  
	        }  
	  
	    }  

}
