import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

import javax.xml.bind.SchemaOutputResolver;
import java.io.FileReader;
import java.util.ArrayList;

public class Main {

    // TODO add plural to ingredients

    @SuppressWarnings("unchecked")
    public static void main(String[] args){
        //Load json ingredients to list
        ArrayList<String> ingredients = new ArrayList<>();
        //Open JSON
        JSONParser parser = new JSONParser();
        try {

            Object obj = parser.parse(new FileReader("ingredientes_pt.json"));
            JSONArray root = (JSONArray) obj;

            //Read ingredients to list
            //int size = 20;
            int size = root.size();
            System.out.println("Now adding ingredients (0/" + root.size() + ")");
            for (int i=0; i<size; i++){
                JSONObject ingredient = (JSONObject) root.get(i);
                //Get the name
                ingredients.add((String) ingredient.get("searchValue"));
                System.out.println("Now adding ingredients (" + (i+1) + "/" + root.size() + ")");
            }

            //Find ingredients in each recipe and add string to new element in each recipe
            obj = parser.parse(new FileReader("receitas.json"));
            root = (JSONArray) obj;

            size = 200;
            System.out.println("Now finding ingredient in recipe (0/" + root.size() + ")");

            for (int i=0; i<size; i++){
                JSONObject recipe = (JSONObject) root.get(i);
                JSONArray secao = (JSONArray) recipe.get("secao");
                JSONObject ingredientsObj = (JSONObject) secao.get(0);
                JSONArray list = (JSONArray) ingredientsObj.get("conteudo");
                //Find matches
                for (int k=0; k<list.size(); k++){
                    String element = (String) list.get(k);
                    //Tokenize array
                    String[] tokens = element.split(" ");
                    //For each token, check if it exists in ingredients
                    ArrayList<String> newList = new ArrayList<>();
                    for (String s:tokens){
                        if (ingredients.contains(s)){
                            newList.add(s);
                        }
                    }

                    //Add to the recipe if not empty
                    if (!newList.isEmpty()){
                        ingredientsObj.put("ingredientes", newList.toArray());
                    }
                }
                ingredients.add((String) recipe.get("searchValue"));
                System.out.println("Now finding ingredient in recipe (" + (i+1) + "/" + root.size() + ")");
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
