import java.io.IOException;  
import jeasy.analysis.MMAnalyzer;  
import java.io.FileNotFoundException;  
import java.io.FileReader; 

public class JeAnalysis {
	 public static void main(String[] args) {  

	        String text = "ȫ�ļ�����ָ�������������ͨ��ɨ�������е�ÿһ���ʣ���ÿһ���ʽ���һ��������" +  
	                "ָ���ô��������г��ֵĴ�����λ�ã����û���ѯʱ����������͸������Ƚ������������в��ң�" +  
	                "�������ҵĽ���������û��ļ�����ʽ���������������ͨ���ֵ��еļ����ֱ���ֵĹ��̡�";  
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
