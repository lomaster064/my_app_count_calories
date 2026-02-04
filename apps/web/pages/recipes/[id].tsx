import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import Layout from "../../components/Layout";
import { apiBaseUrl } from "../../utils/api";

interface Recipe {
  id: number;
  name: string;
  description: string;
  calories: number;
  protein: number;
  fat: number;
  carbs: number;
  ingredients: { name: string; grams: number }[];
  instructions: string[];
}

export default function RecipePage() {
  const router = useRouter();
  const { id } = router.query;
  const [recipe, setRecipe] = useState<Recipe | null>(null);

  useEffect(() => {
    if (!id) return;
    const loadRecipe = async () => {
      const response = await fetch(`${apiBaseUrl()}/recipes/${id}`);
      if (response.ok) {
        setRecipe(await response.json());
      }
    };
    loadRecipe();
  }, [id]);

  return (
    <Layout>
      <h1>Рецепт</h1>
      {recipe && (
        <div className="card">
          <h2>{recipe.name}</h2>
          <p>{recipe.description}</p>
          <p>
            {recipe.calories} ккал · Б {recipe.protein} · Ж {recipe.fat} · У {recipe.carbs}
          </p>
          <h3>Ингредиенты</h3>
          <ul>
            {recipe.ingredients.map((ingredient) => (
              <li key={ingredient.name}>
                {ingredient.name} — {ingredient.grams} г
              </li>
            ))}
          </ul>
          <h3>Шаги</h3>
          <ol>
            {recipe.instructions.map((step) => (
              <li key={step}>{step}</li>
            ))}
          </ol>
        </div>
      )}
    </Layout>
  );
}
